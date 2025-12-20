# backend/ops/tests/models/test_task_model.py
from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from ops.models import Department, Item, DepartmentItemAssignment, Task



def _dt(y, m, d, hh, mm):
    # テスト用の aware datetime を作る
    return timezone.make_aware(datetime(y, m, d, hh, mm))



def _make_assignment(department_name: str, item_name: str, pack_g: int) -> DepartmentItemAssignment:
    department = Department.objects.create(name=department_name)

    item = Item.objects.create(name=item_name, pack_g=pack_g)

    return DepartmentItemAssignment.objects.create(department=department, item=item)



def _make_task(*, required_units=1, started_at=None, finished_at=None) -> Task:
    assignment = _make_assignment("ライン班", "ポテトサラダセット", 1000)
    pickup_at = _dt(2025, 12, 20, 5, 0)

    return Task\
    (
        assignment=assignment,
        pickup_at=pickup_at,
        required_units=required_units,
        started_at=started_at,
        finished_at=finished_at,
    )



# 正常系
@pytest.mark.django_db
def test_task_can_be_created_and_string_is_readable():
    # Arrange
    task = _make_task(required_units=1)



    # Act
    task.full_clean()

    task.save()



    # Assert
    assert Task.objects.filter(pk=task.pk).exists()

    assert task.required_units == 1

    # 読めることだけ確認
    # 文字列の厳密比較は壊れやすい
    assert str(task)



# 異常系: assignment は必須
@pytest.mark.django_db
def test_task_requires_assignment():
    # Arrange
    task = _make_task(required_units=1)

    task.assignment = None



    # Act / Assert
    with pytest.raises(ValidationError):
        task.full_clean()



# 異常系: pickup_at は必須
@pytest.mark.django_db
def test_task_requires_pickup_at():
    # Arrange
    task = _make_task(required_units=1)
    task.pickup_at = None



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
    task = _make_task(required_units=units)



    # Act / Assert
    with pytest.raises(ValidationError):
        task.full_clean()



# 異常系: finished_at は started_at 以降
@pytest.mark.django_db
def test_task_finished_at_must_be_after_started_at():
    # Arrange
    started_at = _dt(2025, 12, 20, 10, 0)
    finished_at = _dt(2025, 12, 20, 9, 0)

    task = _make_task(required_units=1, started_at=started_at, finished_at=finished_at)



    # Act / Assert
    with pytest.raises(ValidationError):
        task.full_clean()



# 異常系: (assignment, pickup_at) はユニーク
@pytest.mark.django_db
def test_task_assignment_and_pickup_at_must_be_unique():
    # Arrange
    task1 = _make_task(required_units=1)

    task1.full_clean()
    task1.save()

    duplicated = Task\
    (
        assignment=task1.assignment,
        pickup_at=task1.pickup_at,
        required_units=1,
    )



    # Act / Assert

    # full_clean() では拾えない場合があるので
    # DB 制約で落とす
    with pytest.raises(IntegrityError):
        duplicated.save()
