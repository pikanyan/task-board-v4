# backend/ops/models/department_item_assignment.py
from django.db import models
from django.core.exceptions import ValidationError

from .department import Department
from .item import Item



class DepartmentItemAssignment(models.Model):
    department = models.ForeignKey\
    (
        Department,
        on_delete=models.PROTECT,
        related_name="item_assignments",
    )

    item = models.ForeignKey\
    (
        Item,
        on_delete=models.PROTECT,
        related_name="department_assignments",
    )



    def __str__(self) -> str:
        return f"{self.department.name}: {self.item.name}"



    def clean(self):
        super().clean()

        errors = {}



        if self.department_id is None:
            errors["department"] = "department は必須です。"

        if self.item_id is None:
            errors["item"] = "item は必須です。"



        if errors:
            raise ValidationError(errors)



    class Meta:
        constraints =\
        [
            models.UniqueConstraint
            (
                fields=["department", "item"],

                name="uniq_department_item_assignment",
            ),
        ]
