# backend/ops/tests/services/test_task_deriver.py
import pytest
from django.utils import timezone

from ops.models.customer import Customer
from ops.models.department import Department
from ops.models.item import Item
from ops.models.department_item_assignment import DepartmentItemAssignment
from ops.models.department_item_assignment_component import DepartmentItemAssignmentComponent
from ops.models.order_header import OrderHeader
from ops.models.order_line import OrderLine
from ops.models.task import Task


from ops.services.task_deriver import derive_tasks_for_order_header



@pytest.mark.django_db
def test_derive_tasks_creates_root_task_only():
    # Arrange
    dept = Department.objects.create(name="ライン班")
    product = Item.objects.create(name="ポテトサラダセット", pack_g=1000)
    assignment = DepartmentItemAssignment.objects.create(department=dept, item=product)

    customer = Customer.objects.create(name="オークワ 田原本店")
    pickup_at = timezone.now()
    header = OrderHeader.objects.create(customer=customer, ordered_at=pickup_at, pickup_at=pickup_at)



    OrderLine.objects.create(order_header=header, product_item=product, quantity_units=1)



    # Act
    derive_tasks_for_order_header(order_header_id=header.id)



    # Assert
    task = Task.objects.get(assignment=assignment, pickup_at=pickup_at)

    assert task.required_units == 1




@pytest.mark.django_db
def test_derive_tasks_expands_components_one_level():
    # Arrange
    dept_line = Department.objects.create(name="ライン班")
    dept_pack = Department.objects.create(name="梱包班")

    item_set = Item.objects.create(name="ポテトサラダセット", pack_g=1000)
    item_base = Item.objects.create(name="ポテトサラダベース", pack_g=800)
    item_lettuce = Item.objects.create(name="レタス (カット)", pack_g=50)



    asg_set = DepartmentItemAssignment.objects.create(department=dept_line, item=item_set)
    asg_base = DepartmentItemAssignment.objects.create(department=dept_pack, item=item_base)
    asg_lettuce = DepartmentItemAssignment.objects.create(department=dept_pack, item=item_lettuce)



    DepartmentItemAssignmentComponent.objects.create\
    (
        parent_department_item_assignment=asg_set,
        child_department_item_assignment=asg_base,
        child_units_per_parent_unit=1,
    )

    DepartmentItemAssignmentComponent.objects.create\
    (
        parent_department_item_assignment=asg_set,
        child_department_item_assignment=asg_lettuce,
        child_units_per_parent_unit=2,
    )



    customer = Customer.objects.create(name="オークワ 田原本店")

    pickup_at = timezone.now()

    header = OrderHeader.objects.create(customer=customer, ordered_at=pickup_at, pickup_at=pickup_at)

    OrderLine.objects.create(order_header=header, product_item=item_set, quantity_units=3)



    # Act
    derive_tasks_for_order_header(order_header_id=header.id)



    # Assert
    assert Task.objects.get(assignment=asg_set, pickup_at=pickup_at).required_units == 3

    assert Task.objects.get(assignment=asg_base, pickup_at=pickup_at).required_units == 3
    
    assert Task.objects.get(assignment=asg_lettuce, pickup_at=pickup_at).required_units == 6



@pytest.mark.django_db
def test_derive_tasks_expands_components_two_levels():
    # Arrange
    dept_line = Department.objects.create(name="ライン班")
    dept_pack = Department.objects.create(name="梱包班")
    dept_potato = Department.objects.create(name="いも班")

    item_set = Item.objects.create(name="ポテトサラダセット", pack_g=1000)
    item_base = Item.objects.create(name="ポテトサラダベース", pack_g=800)
    item_potato_cut = Item.objects.create(name="じゃがいも (乱切り)", pack_g=550)



    asg_set = DepartmentItemAssignment.objects.create(department=dept_line, item=item_set)
    asg_base = DepartmentItemAssignment.objects.create(department=dept_pack, item=item_base)
    asg_potato = DepartmentItemAssignment.objects.create(department=dept_potato, item=item_potato_cut)



    # set -> base (1)
    DepartmentItemAssignmentComponent.objects.create\
    (
        parent_department_item_assignment=asg_set,
        child_department_item_assignment=asg_base,
        child_units_per_parent_unit=1,
    )

    # base -> potato (1)
    DepartmentItemAssignmentComponent.objects.create\
    (
        parent_department_item_assignment=asg_base,
        child_department_item_assignment=asg_potato,
        child_units_per_parent_unit=1,
    )



    customer = Customer.objects.create(name="オークワ 田原本店")

    pickup_at = timezone.now()

    header = OrderHeader.objects.create(customer=customer, ordered_at=pickup_at, pickup_at=pickup_at)

    OrderLine.objects.create(order_header=header, product_item=item_set, quantity_units=3)



    # Act
    derive_tasks_for_order_header(order_header_id=header.id)



    # Assert
    assert Task.objects.get(assignment=asg_set, pickup_at=pickup_at).required_units == 3

    assert Task.objects.get(assignment=asg_base, pickup_at=pickup_at).required_units == 3

    assert Task.objects.get(assignment=asg_potato, pickup_at=pickup_at).required_units == 3




@pytest.mark.django_db
def test_derive_tasks_expands_components_any_depth():
    # Arrange
    dept_line = Department.objects.create(name="ライン班")
    dept_pack = Department.objects.create(name="梱包班")
    dept_potato = Department.objects.create(name="いも班")

    item_set = Item.objects.create(name="ポテトサラダセット", pack_g=1000)
    item_base = Item.objects.create(name="ポテトサラダベース", pack_g=800)
    item_mash = Item.objects.create(name="じゃがいも (マッシュ)", pack_g=550)
    item_cut = Item.objects.create(name="じゃがいも (乱切り)", pack_g=550)



    asg_set = DepartmentItemAssignment.objects.create(department=dept_line, item=item_set)
    asg_base = DepartmentItemAssignment.objects.create(department=dept_pack, item=item_base)
    asg_mash = DepartmentItemAssignment.objects.create(department=dept_pack, item=item_mash)
    asg_cut = DepartmentItemAssignment.objects.create(department=dept_potato, item=item_cut)



    # 3 段以上
    # set -> base -> mash -> cut
    DepartmentItemAssignmentComponent.objects.create\
    (
        parent_department_item_assignment=asg_set,
        child_department_item_assignment=asg_base,
        child_units_per_parent_unit=1,
    )

    DepartmentItemAssignmentComponent.objects.create\
    (
        parent_department_item_assignment=asg_base,
        child_department_item_assignment=asg_mash,
        child_units_per_parent_unit=1,
    )

    DepartmentItemAssignmentComponent.objects.create\
    (
        parent_department_item_assignment=asg_mash,
        child_department_item_assignment=asg_cut,
        child_units_per_parent_unit=1,
    )



    customer = Customer.objects.create(name="オークワ 田原本店")

    pickup_at = timezone.now()

    header = OrderHeader.objects.create(customer=customer, ordered_at=pickup_at, pickup_at=pickup_at)

    OrderLine.objects.create(order_header=header, product_item=item_set, quantity_units=5)



    # Act
    derive_tasks_for_order_header(order_header_id=header.id)



    # Assert
    assert Task.objects.get(assignment=asg_set, pickup_at=pickup_at).required_units == 5

    assert Task.objects.get(assignment=asg_base, pickup_at=pickup_at).required_units == 5

    assert Task.objects.get(assignment=asg_mash, pickup_at=pickup_at).required_units == 5

    assert Task.objects.get(assignment=asg_cut, pickup_at=pickup_at).required_units == 5
