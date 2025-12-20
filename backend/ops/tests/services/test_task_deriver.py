# backend/ops/tests/services/test_task_deriver.py
import pytest
from django.utils import timezone

from ops.models.customer import Customer
from ops.models.department import Department
from ops.models.item import Item
from ops.models.department_item_assignment import DepartmentItemAssignment
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
