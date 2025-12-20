# backend/ops/models/task.py
from django.db import models
from django.core.exceptions import ValidationError

from .department_item_assignment import DepartmentItemAssignment



class Task(models.Model):
    # 集計キーを Task 自体に持たせる
    assignment = models.ForeignKey\
    (
        DepartmentItemAssignment,
        on_delete=models.PROTECT,
        related_name="tasks",
    )

    pickup_at = models.DateTimeField()

    required_units = models.IntegerField()

    # 手入力想定なので nullable
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)



    class Meta:
        # 集計単位の一意性をここで保証
        constraints =\
        [
            models.UniqueConstraint
            (
                fields=["assignment", "pickup_at"],

                name="uq_task_assignment_pickup_at",
            )
        ]



    def __str__(self) -> str:
        return f"{self.assignment} pickup {self.pickup_at} required {self.required_units}"



    def clean(self):
        super().clean()

        errors = {}



        # 必須チェック
        if self.assignment_id is None:
            errors["assignment"] = "assignment は必須です。"

        if self.pickup_at is None:
            errors["pickup_at"] = "pickup_at は必須です。"

        # required_units
        if self.required_units is None:
            errors["required_units"] = "required_units は必須です。"

        elif self.required_units <= 0:
            errors["required_units"] = "required_units は 1 以上にしてください。"

        # 実績の整合性
        if self.started_at is not None and self.finished_at is not None:
            if self.started_at > self.finished_at:
                errors["finished_at"] = "finished_at は started_at 以降にしてください。"



        if errors:
            raise ValidationError(errors)
