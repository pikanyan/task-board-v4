# backend/ops/models/task_plan.py
from django.db import models
from django.core.exceptions import ValidationError

from .task import Task



class TaskPlan(models.Model):
    task = models.OneToOneField\
    (
        Task,
        on_delete=models.CASCADE,
        related_name="plan",
    )



    planned_started_at = models.DateTimeField()
    planned_finished_at = models.DateTimeField()



    # 間に合うなら True
    # 無理なら False
    is_feasible = models.BooleanField(default=True)



    def __str__(self) -> str:
        return f"{self.task_id} {self.planned_started_at} - {self.planned_finished_at}"



    def clean(self):
        super().clean()

        errors = {}



        if self.task_id is None:
            errors["task"] = "task は必須です。"

        if self.planned_started_at is None:
            errors["planned_started_at"] = "planned_started_at は必須です。"

        if self.planned_finished_at is None:
            errors["planned_finished_at"] = "planned_finished_at は必須です。"

        if self.planned_started_at is not None and self.planned_finished_at is not None:
            if self.planned_started_at > self.planned_finished_at:
                errors["planned_finished_at"] = "planned_finished_at は planned_started_at 以降にしてください。"



        if errors:
            raise ValidationError(errors)
