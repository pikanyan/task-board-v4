# backend/ops/tests/models/test_department_item_assignment_component_model.py
import pytest
from django.core.exceptions import ValidationError

from ops.models import\
(
    Department,
    Item,
    DepartmentItemAssignment,
    DepartmentItemAssignmentComponent,
)



def _make_assignment(department_name: str, item_name: str, pack_g: int) -> DepartmentItemAssignment:
    department = Department.objects.create(name=department_name)

    item = Item.objects.create(name=item_name, pack_g=pack_g)

    return DepartmentItemAssignment.objects.create(department=department, item=item)



# 正常系
@pytest.mark.django_db
def test_department_item_assignment_component_can_be_created_and_string_is_readable():
    # Arrange
    parent = _make_assignment("ライン班", "ポテトサラダセット", 1000)
    child = _make_assignment("梱包班", "ポテトサラダベース", 800)

    component = DepartmentItemAssignmentComponent\
    (
        parent_department_item_assignment=parent,
        child_department_item_assignment=child,
        child_units_per_parent_unit=1,
    )



    # Act
    component.full_clean()

    component.save()



    # Assert
    assert DepartmentItemAssignmentComponent.objects.filter(pk=component.pk).exists()

    assert component.parent_department_item_assignment_id == parent.id
    assert component.child_department_item_assignment_id == child.id
    assert component.child_units_per_parent_unit == 1

    assert str(component) == f"{parent} -> {child} x 1"




# 異常系: (parent, child) に関するユニーク制約
@pytest.mark.django_db
def test_department_item_assignment_component_pair_must_be_unique():
    # Arrange
    parent = _make_assignment("ライン班", "ポテトサラダセット", 1000)
    child = _make_assignment("梱包班", "ポテトサラダベース", 800)

    DepartmentItemAssignmentComponent.objects.create\
    (
        parent_department_item_assignment=parent,
        child_department_item_assignment=child,
        child_units_per_parent_unit=1,
    )

    duplicated = DepartmentItemAssignmentComponent(
        parent_department_item_assignment=parent,
        child_department_item_assignment=child,
        child_units_per_parent_unit=1,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        duplicated.full_clean()



# 異常系: parent と child は必須
@pytest.mark.parametrize\
(
    "parent_is_none,child_is_none",
    [
        (True, False),
        (False, True),
        (True, True),
    ],
)
@pytest.mark.django_db
def test_department_item_assignment_component_requires_foreign_keys(parent_is_none, child_is_none):
    # Arrange
    parent = None if parent_is_none else _make_assignment("ライン班", "ポテトサラダセット", 1000)

    child = None if child_is_none else _make_assignment("梱包班", "ポテトサラダベース", 800)

    component = DepartmentItemAssignmentComponent\
    (
        parent_department_item_assignment=parent,
        child_department_item_assignment=child,
        child_units_per_parent_unit=1,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        component.full_clean()



# 異常系: child_units_per_parent_unit の必須/下限チェック
@pytest.mark.parametrize\
(
    "units",

    [
        None,
        0,
        -1
    ],
)
@pytest.mark.django_db
def test_department_item_assignment_component_requires_positive_units(units):
    # Arrange
    parent = _make_assignment("ライン班", "ポテトサラダセット", 1000)
    child = _make_assignment("梱包班", "ポテトサラダベース", 800)

    component = DepartmentItemAssignmentComponent(
        parent_department_item_assignment=parent,
        child_department_item_assignment=child,
        child_units_per_parent_unit=units,
    )

    # Act / Assert
    with pytest.raises(ValidationError):
        component.full_clean()



# 異常系: parent と child の同一を禁止 (自己参照禁止)
@pytest.mark.django_db
def test_department_item_assignment_component_cannot_reference_itself():
    # Arrange
    same = _make_assignment("ライン班", "ポテトサラダセット", 1000)

    component = DepartmentItemAssignmentComponent\
    (
        parent_department_item_assignment=same,
        child_department_item_assignment=same,
        child_units_per_parent_unit=1,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        component.full_clean()
