from django.db import models

from core.models import BaseModel


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "category"


class Product(BaseModel):
    title = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.CharField(max_length=20)
    size = models.CharField(max_length=30)
    pages = models.PositiveIntegerField()
    published_date = models.CharField(max_length=20)
    isbn = models.CharField(max_length=20)
    description = models.TextField()
    issue_number = models.PositiveIntegerField()
    product_image_url = models.CharField(max_length=200)
    main_category = models.ForeignKey(
        Category, null=True, on_delete=models.CASCADE, related_name="main_category_product"
    )
    sub_category = models.ForeignKey(
        Category, null=True, on_delete=models.CASCADE, related_name="sub_category_product"
    )

    class Meta:
        db_table = "product"


class ProductImage(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    main_url = models.CharField(max_length=200)
    sub_url = models.CharField(max_length=200)

    class Meta:
        db_table = "product_image"
