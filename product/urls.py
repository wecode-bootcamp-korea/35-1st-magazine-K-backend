from django.urls import path

from .views import CategoryAPI, ProductAPI, get_product_list

urlpatterns = [
    path("product/", ProductAPI.as_view()),
    path("category/", CategoryAPI.as_view()),
]
