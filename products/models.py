from django.db import models

from core.models import TimeStampModel

class MainCategory(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    name          = models.CharField(max_length=20)

    class Meta:
        db_table = 'sub_categories'

class Product(TimeStampModel):
    title             = models.CharField(max_length=30)
    price             = models.DecimalField(max_digits=10, decimal_places=2)
    language          = models.CharField(max_length=20)
    size              = models.CharField(max_length=30)
    pages             = models.PositiveIntegerField()
    date              = models.CharField(max_length=20)
    isbn              = models.CharField(max_length=20)
    description       = models.TextField(blank=False)
    issue_number      = models.PositiveIntegerField()
    product_image_url = models.CharField(max_length=200)
    sub_category      = models.ManyToManyField(SubCategory, through='SubCateGoryProduct', related_name='product')

    class Meta:
        db_table = 'products'

class SubCateGoryProduct(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories_products'

class ProductImage(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    main_url = models.CharField(max_length=200)
    sub_url  = models.CharField(max_length=200)

    class Meta:
        db_table = 'products_images'