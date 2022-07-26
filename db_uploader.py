import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "magazinek.settings")

django.setup()

from products.models import Category, Product, ProductImage
from orders.models   import OrderStatus

CSV_PATH_CATEGORIES          = './csv/categories.csv'
CSV_PATH_PRODUCTS            = './csv/products.csv'
CSV_PATH_CATEGORIES_PRODUCTS = './csv/categories_products.csv'
CSV_PATH_PRODUCT_IMAGES      = './csv/product_images.csv'
CSV_PATH_ORDER_STATUS        = './csv/order_statuses.csv'

with open(CSV_PATH_CATEGORIES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            Category.objects.create(
                name = row[0],
            )

with open(CSV_PATH_PRODUCTS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            Product.objects.create(
                title             = row[0],
                price             = row[1],
                language          = row[2],
                size              = row[3],
                pages             = row[4],
                published_date    = row[5],
                isbn              = row[6],
                description       = row[7],
                issue_number      = row[8],
                product_image_url = row[9],
                main_category     = Category.objects.get(id=row[10]),
                sub_category      = Category.objects.get(id=row[11]),
            )

with open(CSV_PATH_PRODUCT_IMAGES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            ProductImage.objects.create(
                product  = Product.objects.get(id=row[0]),
                main_url = row[1],
                sub_url  = row[2],
            )

with open(CSV_PATH_ORDER_STATUS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            OrderStatus.objects.create(
                order_status = row[0],
            )