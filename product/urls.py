from django.urls import path

from .views import CategoryAPI, ProductAPI, get_product_list

urlpatterns = [
    path("category/", CategoryAPI.as_view()),
    path("category/<int:category_id>/", CategoryAPI.as_view()),
    path("product/", ProductAPI.as_view()),
    path("product/<int:product_id>/", ProductAPI.as_view()),
    path("product/list/", get_product_list),
]
