from django.db import models

from users.models    import User
from products.models import Product
from core.models     import TimeStampModel

class OrderStatus(models.Model):
    order_status = models.CharField(max_length=20)

    class Meta:
        db_table = 'order_statuses'

class Order(TimeStampModel):
    user_id         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_status_id = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    order_number    = models.UUIDField()

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    product_id     = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id       = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField(max_length=3)
    order_price    = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'