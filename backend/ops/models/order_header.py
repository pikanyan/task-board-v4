# backend/ops/models/order_header.py
from django.db import models
from django.core.exceptions import ValidationError

from django.utils import timezone
from django.utils.formats import date_format

from .customer import Customer

from ops.utils.dt import format_dt_jst 



class OrderHeader(models.Model):
    customer = models.ForeignKey\
    (
        Customer,
        on_delete=models.PROTECT,
        related_name="order_headers",
    )

    ordered_at = models.DateTimeField()
    pickup_at = models.DateTimeField()



    def __str__(self) -> str:
        return f"{self.customer.name}: {format_dt_jst(self.pickup_at)}"



    def clean(self):
        super().clean()

        errors = {}



        if self.customer_id is None:
            errors["customer"] = "customer は必須です。"

        if self.ordered_at is None:
            errors["ordered_at"] = "ordered_at は必須です。"

        if self.pickup_at is None:
            errors["pickup_at"] = "pickup_at は必須です。"

        if self.ordered_at is not None and self.pickup_at is not None:
            if self.ordered_at > self.pickup_at:
                errors["ordered_at"] = "ordered_at は pickup_at 以下にしてください。"



        if errors:
            raise ValidationError(errors)
