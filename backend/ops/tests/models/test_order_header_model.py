# backend/ops/tests/models/test_order_header_model.py
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from ops.models import Customer, OrderHeader



def _dt(y, m, d, hh, mm):
    # テスト用の aware datetime を作る
    return timezone.make_aware(datetime(y, m, d, hh, mm))



def _fmt_tokyo(dt):
    # __str__ の表示(= JSTで YYYY-MM-DD HH:MM)に合わせる
    return dt.astimezone(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M")



# 正常系
@pytest.mark.django_db
def test_order_header_can_be_created_and_string_is_readable():
    # Arrange
    customer = Customer.objects.create(name="オークワ 田原本店")

    ordered_at = _dt(2025, 12, 20, 5, 0)
    pickup_at = _dt(2025, 12, 21, 5, 0)

    order = OrderHeader\
    (
        customer=customer,
        ordered_at=ordered_at,
        pickup_at=pickup_at,
    )



    # Act
    order.full_clean()

    order.save()



    # Assert
    assert OrderHeader.objects.filter(pk=order.pk).exists()

    assert order.customer_id == customer.id
    assert order.ordered_at == ordered_at
    assert order.pickup_at == pickup_at



    # 表示は「誰の注文で、いつ引き渡しなのか」が一目で分かること
    assert str(order) == f"{customer.name}: {_fmt_tokyo(pickup_at)}"



# 異常系: customer / ordered_at / pickup_at は必須
@pytest.mark.parametrize\
(
    "customer_is_none,ordered_is_none,pickup_is_none",
    [
        (True, False, False),
        (False, True, False),
        (False, False, True),
        (True, True, True),
    ],
)
@pytest.mark.django_db
def test_order_header_requires_fields(customer_is_none, ordered_is_none, pickup_is_none):
    # Arrange
    customer = None if customer_is_none else Customer.objects.create(name="オークワ 田原本店")

    ordered_at = None if ordered_is_none else _dt(2025, 12, 20, 5, 0)
    pickup_at = None if pickup_is_none else _dt(2025, 12, 21, 5, 0)

    order = OrderHeader\
    (
        customer=customer,
        ordered_at=ordered_at,
        pickup_at=pickup_at,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        order.full_clean()



# 異常系: ordered_at は pickup_at 以下であること
@pytest.mark.django_db
def test_order_header_ordered_at_must_be_before_or_equal_pickup_at():
    # Arrange
    customer = Customer.objects.create(name="オークワ 田原本店")

    ordered_at = _dt(2025, 12, 21, 5, 0)
    pickup_at = _dt(2025, 12, 20, 5, 0)

    order = OrderHeader\
    (
        customer=customer,
        ordered_at=ordered_at,
        pickup_at=pickup_at,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        order.full_clean()
