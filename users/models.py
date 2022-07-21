from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    user_name      = models.CharField(max_length=20, unique=True)
    password       = models.CharField(max_length=200)
    name           = models.CharField(max_length=20)
    zip_code       = models.CharField(max_length=10)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    phone_number   = models.CharField(max_length=50)
    email          = models.EmailField(max_length=50)
    point          = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'users'
