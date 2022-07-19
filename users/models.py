from django.db import models

class TimeStempModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(TimeStempModel):
    user_name      = models.CharField(max_length=20, unique=True)
    password       = models.CharField(max_length=200)
    name           = models.CharField(max_length=20)
    zip_code       = models.CharField(max_length=10)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    phone_number   = models.CharField(max_length=50)
    email          = models.EmailField(max_length=50)
    point          = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = 'users'
