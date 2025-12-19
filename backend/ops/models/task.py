# backend/ops/models/task.py
from django.db import models
from django.core.exceptions import ValidationError

from .task_key import TaskKey



class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "todo"
        DONE = "done", "done"



    # 外部キーの中でも、相手は必ず 1 件だけという制約つき参照
    task_key = models.OneToOneField\
    (
        TaskKey,
        on_delete=models.PROTECT,
        related_name="task",
    )

    required_units = models.IntegerField()

    status = models.CharField\
    (
        max_length=16,
        choices=Status.choices,
        default=Status.TODO,
    )



    def __str__(self) -> str:
        return f"{self.task_key} required {self.required_units} ({self.status})"



    def clean(self):
        super().clean()

        errors = {}



        if self.task_key_id is None:
            errors["task_key"] = "task_key は必須です。"

        if self.required_units is None:
            errors["required_units"] = "required_units は必須です。"

        elif self.required_units <= 0:
            errors["required_units"] = "required_units は 1 以上にしてください。"



        # choices 外チェック
        if self.status is None or self.status == "":
            errors["status"] = "status は必須です。"

        elif self.status not in self.Status.values:
            errors["status"] = "status が不正です。"



        if errors:
            raise ValidationError(errors)
