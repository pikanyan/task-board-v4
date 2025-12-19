# backend/ops/tests/models/test_task_key_model.py
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from ops.models import Department, Item, DepartmentItemAssignment, TaskKey



def _dt(y, m, d, hh, mm):
    # テスト用の aware datetime を作る
    return timezone.make_aware(datetime(y, m, d, hh, mm))



def _fmt_tokyo(dt):
    # __str__ の表示(= JSTで YYYY-MM-DD HH:MM)に合わせる
    return dt.astimezone(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M")



def _make_assignment(department_name: str, item_name: str, pack_g: int) -> DepartmentItemAssignment:
    # DepartmentItemAssignment の最小生成
    department = Department.objects.create(name=department_name)

    item = Item.objects.create(name=item_name, pack_g=pack_g)

    return DepartmentItemAssignment.objects.create(department=department, item=item)




# 正常系
@pytest.mark.django_db
def test_task_key_can_be_created_and_string_is_readable():
    # Arrange
    assignment = _make_assignment("ライン班", "ポテトサラダセット", 1000)
    pickup_at = _dt(2025, 12, 20, 5, 0)

    task_key = TaskKey\
    (
        assignment=assignment,
        pickup_at=pickup_at,
    )



    # Act
    task_key.full_clean()

    task_key.save()



    # Assert
    assert TaskKey.objects.filter(pk=task_key.pk).exists()

    assert task_key.assignment_id == assignment.id
    assert task_key.pickup_at == pickup_at

    assert str(task_key) == f"{assignment} {_fmt_tokyo(pickup_at)}"



# 異常系: (assignment, pickup_at) に関するユニーク制約
@pytest.mark.django_db
def test_task_key_pair_must_be_unique():
    # Arrange
    assignment = _make_assignment("ライン班", "ポテトサラダセット", 1000)

    pickup_at = _dt(2025, 12, 20, 5, 0)

    TaskKey.objects.create\
    (
        assignment=assignment,
        pickup_at=pickup_at,
    )

    duplicated = TaskKey\
    (
        assignment=assignment,
        pickup_at=pickup_at,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        duplicated.full_clean()



# 異常系: assignment と pickup_at は必須
@pytest.mark.parametrize\
(
    "assignment_is_none,pickup_is_none",
    [
        (True, False),
        (False, True),
        (True, True),
    ],
)
@pytest.mark.django_db
def test_task_key_requires_fields(assignment_is_none, pickup_is_none):
    # Arrange
    assignment = None if assignment_is_none else _make_assignment("ライン班", "ポテトサラダセット", 1000)
    pickup_at = None if pickup_is_none else _dt(2025, 12, 20, 5, 0)

    task_key = TaskKey\
    (
        assignment=assignment,
        pickup_at=pickup_at,
    )



    # Act / Assert
    with pytest.raises(ValidationError):
        task_key.full_clean()
