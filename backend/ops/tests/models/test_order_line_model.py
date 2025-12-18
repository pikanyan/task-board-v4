# backend/ops/tests/models/test_order_line_model.py
from datetime import datetime

import pytest

from django.core.exceptions import ValidationError
from django.utils import timezone

from ops.models import Customer, Item, OrderHeader, OrderLine



def _dt(y, m, d, hh, mm):
    # テスト用の aware datetime を作る
    return timezone.make_aware(datetime(y, m, d, hh, mm))



def _make_order_header() -> OrderHeader:
    # OrderHeader の最小生成
    customer = Customer.objects.create(name="オークワ 田原本店")

    ordered_at = _dt(2025, 12, 20, 5, 0)
    pickup_at = _dt(2025, 12, 21, 5, 0)

    return OrderHeader.objects.create\
    (
        customer=customer,
        ordered_at=ordered_at,
        pickup_at=pickup_at,
    )



# 正常系
@pytest.mark.django_db
def test_order_line_can_be_created_and_string_is_readable():
    # Arrange
    header = _make_order_header()

    product_item = Item.objects.create(name="ポテトサラダセット", pack_g=1000)

    line = OrderLine\
    (
        order_header=header,
        product_item=product_item,
        quantity_units=1,
    )



    # Act
    line.full_clean()

    line.save()



    # Assert
    assert OrderLine.objects.filter(pk=line.pk).exists()

    assert line.order_header_id == header.id
    assert line.product_item_id == product_item.id
    assert line.quantity_units == 1

    assert str(line) == f"{header} - {product_item.name} x 1"



# 異常系: order_header / product_item は必須
@pytest.mark.parametrize\
(
    "header_is_none,item_is_none",

    [
        (True, False),
        (False, True),
        (True, True),
    ],
)
@pytest.mark.django_db
def test_order_line_requires_foreign_keys(header_is_none, item_is_none):
    # Arrange
    header = None if header_is_none else _make_order_header()

    product_item = None if item_is_none else Item.objects.create(name="ポテトサラダセット", pack_g=1000)

    line = OrderLine\
    (
        order_header=header,
        product_item=product_item,
        quantity_units=1,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        line.full_clean()


# 異常系: quantity_units の必須/下限チェック
@pytest.mark.parametrize\
(
    "units",

    [
        None,
        0,
        -1,
    ],
)
@pytest.mark.django_db
def test_order_line_requires_units_and_min_value(units):
    # Arrange
    header = _make_order_header()
    product_item = Item.objects.create(name="ポテトサラダセット", pack_g=1000)

    line = OrderLine\
    (
        order_header=header,
        product_item=product_item,
        quantity_units=units,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        line.full_clean()



# 異常系: (order_header, product_item) に関するユニーク制約
@pytest.mark.django_db
def test_order_line_pair_must_be_unique():
    # Arrange
    header = _make_order_header()
    
    product_item = Item.objects.create(name="ポテトサラダセット", pack_g=1000)

    OrderLine.objects.create\
    (
        order_header=header,
        product_item=product_item,
        quantity_units=1,
    )

    duplicated = OrderLine\
    (
        order_header=header,
        product_item=product_item,
        quantity_units=1,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        duplicated.full_clean()
