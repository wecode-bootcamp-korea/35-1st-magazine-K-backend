from django.db import models

from users.models    import User
from products.models import Product
from core.models     import TimeStampModel

class OrderStatus(models.Model):
    order_status = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_statuses'

class Order(TimeStampModel):
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    order_number = models.UUIDField()

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)
    order          = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField()
    order_price    = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'