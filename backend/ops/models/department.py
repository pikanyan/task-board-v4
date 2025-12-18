# backend/ops/models/department.py
from django.db import models
from django.core.exceptions import ValidationError



class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)



    def __str__(self) -> str:
        return self.name



    def clean(self):
        super().clean()

        errors = {}



        if self.name is None or self.name.strip() == "":
            errors["name"] = "name を空白にはできません。"



        if errors:
            raise ValidationError(errors)
