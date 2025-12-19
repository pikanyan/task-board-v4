# backend/ops/tests/admin/test_admin_registered_models.py
import pytest

from django.contrib.admin import site

from ops import models



@pytest.mark.parametrize\
(
    "model",

    [
        models.Customer,
        models.Department,
        models.Item,
        models.DepartmentItemAssignment,
        models.DepartmentItemAssignmentComponent,
        models.OrderHeader,
        models.OrderLine,
        models.TaskKey,
        models.Task,
    ],
)
def test_admin_registers_board_models(model):
    # Arrange



    # Act
    is_registered = model in site._registry



    # Assert
    assert is_registered
