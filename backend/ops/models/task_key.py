# backend/ops/models/task_key.py
from django.db import models
from django.core.exceptions import ValidationError

from django.utils import timezone
from django.utils.formats import date_format

from .department_item_assignment import DepartmentItemAssignment

from ops.utils.dt import format_dt_jst 



class TaskKey(models.Model):
    assignment = models.ForeignKey\
    (
        DepartmentItemAssignment,
        on_delete=models.PROTECT,
        related_name="task_keys",
    )

    pickup_at = models.DateTimeField()



    def __str__(self) -> str:
        return f"{self.assignment} {format_dt_jst(self.pickup_at)}"



    def clean(self):
        super().clean()

        errors = {}



        if self.assignment_id is None:
            errors["assignment"] = "assignment は必須です。"

        if self.pickup_at is None:
            errors["pickup_at"] = "pickup_at は必須です。"

        if errors:
            raise ValidationError(errors)



    class Meta:
        constraints =\
        [
            models.UniqueConstraint
            (
                fields=["assignment", "pickup_at"],
                
                name="uniq_task_key",
            ),
        ]
