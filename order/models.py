from django.db import models

from user.models import User
from product.models import Product
from core.models import BaseModel


class OrderStatus(models.Model):
    order_status = models.CharField(max_length=50)

    class Meta:
        db_table = "order_status"


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    order_number = models.UUIDField(null=True)

    class Meta:
        db_table = "order"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "order_item"
