# backend/ops/models/item.py
from django.db import models
from django.core.exceptions import ValidationError



class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)

    pack_g = models.PositiveIntegerField()



    def __str__(self) -> str:
        return self.name



    def clean(self):
        super().clean()

        errors = {}



        if self.name is None or self.name.strip() == "":
            errors["name"] = "name を空白にはできません。"

        if self.pack_g is None or self.pack_g <= 0:
            errors["pack_g"] = "pack_g は 1 以上が必要です。"



        if errors:
            raise ValidationError(errors)
