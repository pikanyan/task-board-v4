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
        OrderHeader.objects
        .select_related("customer")
        .prefetch_related("lines__product_item")
        .get(id=order_header_id)
    )

    pickup_at = header.pickup_at



    for line in header.lines.all():
        # いったん
        # 「商品 Item に対応する assignment は 1 件だけ」
        # という前提で進める
        qs = DepartmentItemAssignment.objects.filter(item=line.product_item)

        if not qs.exists():
            raise ValidationError(f"DepartmentItemAssignment not found for item={line.product_item.id}")

        if 1 < qs.count():
            raise ValidationError(f"DepartmentItemAssignment is ambiguous for item={line.product_item.id}")

        assignment = qs.get()



        # 既存があれば上書き
        Task.objects.update_or_create\
        (
            assignment=assignment,
            pickup_at=pickup_at,
            defaults={"required_units": line.quantity_units},
        )
