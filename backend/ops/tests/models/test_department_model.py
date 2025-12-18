# backend/ops/tests/models/test_department_model.py
import pytest

from django.core.exceptions import ValidationError

from ops.models import Department



# 正常系
@pytest.mark.django_db
def test_department_can_be_created_and_string_is_name():
    # Arrange
    name = "ライン班"

    department = Department(name=name)



    # Act
    department.full_clean()

    department.save()



    # Assert
    assert Department.objects.filter(pk=department.pk).exists()

    assert department.name == name

    assert str(department) == name



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
def test_department_name_is_required(name):
    # Arrange
    department = Department(name=name)



    # Act / Assert
    with pytest.raises(ValidationError):
        department.full_clean()
