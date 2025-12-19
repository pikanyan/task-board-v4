# backend/ops/tests/models/test_item_model.py
import pytest
from django.core.exceptions import ValidationError

from ops.models import Item


# 正常系
@pytest.mark.django_db
def test_item_can_be_created_and_string_is_name():
    # Arrange
    name = "ポテトサラダセット"
    pack_g = 1000

    item = Item(name=name, pack_g=pack_g)



    # Act
    item.full_clean()

    item.save()



    # Assert
    assert Item.objects.filter(pk=item.pk).exists()

    assert item.name == name
    assert item.pack_g == pack_g

    assert str(item) == f"{name} {pack_g} g"



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
def test_item_name_is_required(name):
    # Arrange
    item = Item(name=name, pack_g=1000)



    # Act / Assert
    with pytest.raises(ValidationError):
        item.full_clean()



# 異常系: pack_g の必須/下限チェック
@pytest.mark.parametrize\
(
    "pack_g",

    [
        None,
        0,
        -1,
    ],
)
@pytest.mark.django_db
def test_item_pack_g_must_be_positive(pack_g):
    # Arrange
    item = Item(name="ポテトサラダセット", pack_g=pack_g)



    # Act / Assert
    with pytest.raises(ValidationError):
        item.full_clean()
