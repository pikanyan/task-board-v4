# backend/ops/tests/models/test_customer_model.py
import pytest

from django.core.exceptions import ValidationError

from ops.models import Customer



# 正常系
@pytest.mark.django_db
def test_customer_can_be_created_and_string_is_name():
    # Arrange
    name = "オークワ 田原本店"

    customer = Customer(name=name)



    # Act
    customer.full_clean()

    customer.save()



    # Assert
    assert Customer.objects.filter(pk=customer.pk).exists()

    assert customer.name == name

    assert str(customer) == name




# 異常系: name の必須チェック
@pytest.mark.parametrize\
(
    "name",

    [
        None,
        "",     # 空文字
        " ",    # 半角空白
        "　",   # 全角空白
    ],
)
@pytest.mark.django_db
def test_customer_name_is_required(name):
    # Arrange
    customer = Customer(name=name)



    # Act / Assert
    with pytest.raises(ValidationError):
        # Django のバリデーションを明示的に走らせる
        customer.full_clean()
