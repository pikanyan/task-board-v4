# backend/ops/tests/models/test_task_model.py
from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from ops.models import Department, Item, DepartmentItemAssignment, TaskKey, Task



def _dt(y, m, d, hh, mm):
    # テスト用の aware datetime を作る
    return timezone.make_aware(datetime(y, m, d, hh, mm))



def _make_assignment(department_name: str, item_name: str, pack_g: int) -> DepartmentItemAssignment:
    department = Department.objects.create(name=department_name)

    item = Item.objects.create(name=item_name, pack_g=pack_g)

    return DepartmentItemAssignment.objects.create(department=department, item=item)



def _make_task_key() -> TaskKey:
    assignment = _make_assignment("ライン班", "ポテトサラダセット", 1000)

    pickup_at = _dt(2025, 12, 20, 5, 0)
    
    return TaskKey.objects.create(assignment=assignment, pickup_at=pickup_at)



# 正常系
@pytest.mark.django_db
def test_task_can_be_created_and_string_is_readable():
    # Arrange
    task_key = _make_task_key()

    task = Task\
    (
        task_key=task_key,
        required_units=1,
        status="todo",
    )



    # Act
    task.full_clean()

    task.save()



    # Assert
    assert Task.objects.filter(pk=task.pk).exists()

    assert task.task_key_id == task_key.id
    assert task.required_units == 1
    assert task.status == "todo"

    assert str(task) == f"{task_key} required 1 ({task.status})"



# 異常系: task_key は必須
@pytest.mark.django_db
def test_task_requires_task_key():
    # Arrange
    task = Task\
    (
        task_key=None,
        required_units=1,
        status="todo",
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        task.full_clean()



# 異常系: required_units の必須/下限チェック
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
def test_task_requires_units_and_min_value(units):
    # Arrange
    task_key = _make_task_key()

    task = Task\
    (
        task_key=task_key,
        required_units=units,
        status="todo",
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        task.full_clean()



# 異常系: status は choices 外を禁止
@pytest.mark.django_db
def test_task_status_must_be_valid_choice():
    # Arrange
    task_key = _make_task_key()

    task = Task\
    (
        task_key=task_key,
        required_units=1,

        # todo / done 以外
        status="doing",
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        task.full_clean()



# 異常系: task_key は 1 対 1 (重複禁止)
@pytest.mark.django_db
def test_task_task_key_must_be_unique():
    # Arrange
    task_key = _make_task_key()

    Task.objects.create\
    (
        task_key=task_key,
        required_units=1,
        status="todo",
    )

    duplicated = Task\
    (
        task_key=task_key,
        required_units=1,
        status="todo",
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        duplicated.full_clean()
