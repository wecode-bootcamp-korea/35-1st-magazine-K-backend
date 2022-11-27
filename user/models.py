from django.db import models

from core.models import BaseModel


class User(BaseModel):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10, null=True)
    address_line_1 = models.CharField(max_length=100, null=True)
    address_line_2 = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=50)
    point = models.DecimalField(max_digits=20, decimal_places=2, default=100000)

    class Meta:
        db_table = "user"
