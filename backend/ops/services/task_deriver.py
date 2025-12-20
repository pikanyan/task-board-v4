# backend/ops/tests/services/task_deriver.py
from django.core.exceptions import ValidationError
from django.db import transaction

from ops.models.department_item_assignment import DepartmentItemAssignment
from ops.models.order_header import OrderHeader
from ops.models.task import Task



"""
python backend/manage.py shell



from ops.models.order_header import OrderHeader
from ops.models.task import Task
from ops.services.task_deriver import derive_tasks_for_order_header

h = OrderHeader.objects.order_by("-id").first()
derive_tasks_for_order_header(order_header_id=h.id)

Task.objects.filter(pickup_at=h.pickup_at).order_by("assignment_id").values("assignment_id","required_units")
"""


"""
できれば、
shell ではなく
管理画面で実行できるようにする
"""



@transaction.atomic
def derive_tasks_for_order_header(*, order_header_id: int) -> None:
    """
    OrderLine の product_item に対応する assignment を 1 段だけ探して Task を作る

    NOTE: Component 展開は未実装
    """
    header =\
    (
        # FROM order_header
        OrderHeader.objects

        # JOIN customer ON customer.id = order_header.customer_id;
        .select_related("customer")

        # 一気に取得することで N+1 回避
        # lines は OrderLine への逆参照
        .prefetch_related("lines__product_item")

        # WHERE order_header.id = ? して 1 件取る
        .get(id=order_header_id)
    )

    pickup_at = header.pickup_at



    for line in header.lines.all():
        # filter() は検索条件を作成しただけであり
        # 1 件のレコードは未確定
        qs = DepartmentItemAssignment.objects.filter(item=line.product_item)



        if not qs.exists():
            raise ValidationError(f"DepartmentItemAssignment not found for item={line.product_item.id}")

        if 1 < qs.count():
            raise ValidationError(f"DepartmentItemAssignment is ambiguous for item={line.product_item.id}")



        # get() でレコードを 1 件取得
        assignment = qs.get()



        # 既存があれば上書き
        Task.objects.update_or_create\
        (
            # レコードを探す為の複合 key (assignment, pickup_at)
            assignment=assignment,
            pickup_at=pickup_at,

            # 値を更新
            defaults={"required_units": line.quantity_units},
        )




"""
SQL の JOIN 結果



order_header

id	customer_id	pickup_at
10	1	        2025-12-21 05:00



order_line

id	order_header_id	product_item_id	quantity_units
100	10	            1	            1
101	10	            3	            2



SELECT
    oh.id AS header_id, oh.pickup_at, ol.id AS line_id, ol.product_item_id, ol.quantity_units
FROM
    order_header oh

JOIN
    order_line ol
ON
    ol.order_header_id = oh.id;



header_id	pickup_at	        line_id	product_item_id	quantity_units
10	        2025-12-21 05:00	100	    1	            1
10	        2025-12-21 05:00	101	    3	            2
"""



"""
prefetch はの結果
親 1 行 + 子リスト



OrderHeader オブジェクト

フィールド	値
id	        10
pickup_at	2025-12-21 05:00
lines	    [(OrderLine id=100), (OrderLine id=101)]



lines の中身

line.id	product_item_id	quantity_units
100	    1	            1
101 	3	            2



親の行は 1 回だけ
子は「親の中にリスト」として格納

表が 1 枚になるわけじゃない
"""



"""
prefetch_related("lines__product_item") なし

header = ...get(...)
OrderHeader + customer を取り、JOIN
OrderLine + Item は取らない

header.lines.all()
OrderLine を取る SQL が 1 回走る

line.product_item
Item を取る SQL が明細の数だけ走る可能性がある
N+1 の芽がある



prefetch_related("lines__product_item") あり

header = ...get(...)
OrderHeader + customer を取り、JOIN
OrderLine + Item を取る SQL がそれぞれ 1 回走る

header.lines.all()
OrderLine を取る SQL が走らない

line.product_item
Item を取る SQL が走らない
N+1 の芽がない
"""
