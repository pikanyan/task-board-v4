# backend/ops/models/department_item_assignment_component.py
from django.db import models
from django.core.exceptions import ValidationError

from .department_item_assignment import DepartmentItemAssignment



class DepartmentItemAssignmentComponent(models.Model):
    parent_department_item_assignment = models.ForeignKey\
    (
        DepartmentItemAssignment,
        on_delete=models.PROTECT,
        related_name="components_as_parent",
    )

    child_department_item_assignment = models.ForeignKey\
    (
        DepartmentItemAssignment,
        on_delete=models.PROTECT,
        related_name="components_as_child",
    )

    child_units_per_parent_unit = models.IntegerField()



    def __str__(self) -> str:
        return\
        (
            f"{self.parent_department_item_assignment} -> "
            f"{self.child_department_item_assignment} x "
            f"{self.child_units_per_parent_unit}"
        )

    def clean(self):
        super().clean()

        errors = {}



        if self.parent_department_item_assignment_id is None:
            errors["parent_department_item_assignment"] = "parent_department_item_assignment は必須です。"

        if self.child_department_item_assignment_id is None:
            errors["child_department_item_assignment"] = "child_department_item_assignment は必須です。"



        # 必須/下限チェック
        if self.child_units_per_parent_unit is None:
            errors["child_units_per_parent_unit"] = "child_units_per_parent_unit は必須です。"
            
        elif self.child_units_per_parent_unit <= 0:
            errors["child_units_per_parent_unit"] = "child_units_per_parent_unit は 1 以上にしてください。"



        # 自己参照禁止
        if\
        (
            self.parent_department_item_assignment_id is not None
            and
            self.child_department_item_assignment_id is not None
            and
            self.parent_department_item_assignment_id == self.child_department_item_assignment_id
        ):
            errors["child_department_item_assignment"] = "parent と child に同じ割当は指定できません。"



        if errors:
            raise ValidationError(errors)



    class Meta:
        constraints =\
        [
            models.UniqueConstraint
            (
                fields=["parent_department_item_assignment", "child_department_item_assignment"],

                name="uniq_department_item_assignment_component",
            ),
        ]
