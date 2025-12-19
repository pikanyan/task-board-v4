# backend/ops/tests/models/test_department_item_assignment_model.py
import pytest
from django.core.exceptions import ValidationError

from ops.models import Department, Item, DepartmentItemAssignment



# 正常系
@pytest.mark.django_db
def test_department_item_assignment_can_be_created_and_string_is_readable():
    # Arrange
    department = Department.objects.create(name="ライン班")
    item = Item.objects.create(name="ポテトサラダセット", pack_g=1000)

    assignment = DepartmentItemAssignment(department=department, item=item)



    # Act
    assignment.full_clean()

    assignment.save()



    # Assert
    assert DepartmentItemAssignment.objects.filter(pk=assignment.pk).exists()

    assert assignment.department_id == department.id
    assert assignment.item_id == item.id


    assert str(assignment) == f"{department.name}: {item.name} {item.pack_g} g"



# 異常系: (department, item) に関するユニーク制約
@pytest.mark.django_db
def test_department_item_assignment_pair_must_be_unique():
    # Arrange
    department = Department.objects.create(name="ライン班")

    item = Item.objects.create(name="ポテトサラダセット", pack_g=1000)

    DepartmentItemAssignment.objects.create(department=department, item=item)

    duplicated = DepartmentItemAssignment(department=department, item=item)



    # Act / Assert
    with pytest.raises(ValidationError):
        duplicated.full_clean()



# 異常系: department と item は必須
@pytest.mark.parametrize\
(
    "department_is_none,item_is_none",

    [
        (True, False),
        (False, True),
        (True, True),
    ],
)
@pytest.mark.django_db
def test_department_item_assignment_requires_foreign_keys(department_is_none, item_is_none):
    # Arrange
    department = None if department_is_none else Department.objects.create(name="ライン班")

    item = None if item_is_none else Item.objects.create(name="ポテトサラダセット", pack_g=1000)

    assignment = DepartmentItemAssignment(department=department, item=item)



    # Act / Assert
    with pytest.raises(ValidationError):
        assignment.full_clean()
