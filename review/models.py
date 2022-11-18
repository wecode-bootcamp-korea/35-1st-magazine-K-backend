from django.db import models

from core.models import BaseModel
from user.models import User
from product.models import Product


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        db_table = "review"
