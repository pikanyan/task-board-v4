# backend/ops/tests/models/test_task_plan_model.py

import pytest
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from ops import models as m



def _create_task(*, required_units: int = 1, pickup_at=None) -> m.Task:
    if pickup_at is None:
        pickup_at = timezone.now()



    department = m.Department.objects.create(name="ライン班")
    item = m.Item.objects.create(name="ポテトサラダセット", pack_g=1000)

    assignment = m.DepartmentItemAssignment.objects.create(department=department, item=item)



    return m.Task.objects.create\
    (
        assignment=assignment,
        pickup_at=pickup_at,
        required_units=required_units,
    )



@pytest.mark.django_db
def test_taskplan_valid_ok():
    # Arrange
    task = _create_task()

    start = timezone.now()
    finish = start + timedelta(minutes=10)



    # Act
    plan = m.TaskPlan\
    (
        task=task,

        planned_started_at=start,
        planned_finished_at=finish,

        is_feasible=True,
    )



    # Assert

    # 例外が出なければ OK
    plan.full_clean()



@pytest.mark.django_db
def test_taskplan_invalid_when_started_after_finished():
    # Arrange
    task = _create_task()

    start = timezone.now()
    finish = start - timedelta(minutes=10)



    # Act
    plan = m.TaskPlan\
    (
        task=task,

        planned_started_at=start,
        planned_finished_at=finish,

        is_feasible=False,
    )



    # Assert
    with pytest.raises(ValidationError):
        plan.full_clean()
