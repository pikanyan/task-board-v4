# backend/ops/models/order_line.py
from django.db import models
from django.core.exceptions import ValidationError

from .item import Item
from .order_header import OrderHeader



class OrderLine(models.Model):
    order_header = models.ForeignKey\
    (
        OrderHeader,
        on_delete=models.PROTECT,
        related_name="lines",
    )

    product_item = models.ForeignKey\
    (
        Item,
        on_delete=models.PROTECT,
        related_name="order_lines_as_product",
    )

    quantity_units = models.IntegerField()



    def __str__(self) -> str:
        return f"{self.order_header} - {self.product_item.name} x {self.quantity_units}"



    def clean(self):
        super().clean()

        errors = {}



        if self.order_header_id is None:
            errors["order_header"] = "order_header は必須です。"

        if self.product_item_id is None:
            errors["product_item"] = "product_item は必須です。"

        if self.quantity_units is None:
            errors["quantity_units"] = "quantity_units は必須です。"
        elif self.quantity_units <= 0:
            errors["quantity_units"] = "quantity_units は 1 以上にしてください。"



        if errors:
            raise ValidationError(errors)



    class Meta:
        constraints =\
        [
            models.UniqueConstraint
            (
                fields=["order_header", "product_item"],
                
                name="uniq_order_line",
            ),
        ]
