from django.urls import path

from product.views import ProductView, ProductDetailView, ProductManageView

urlpatterns = [
    path("", ProductView.as_view()),
    path("<int:product_id>/", ProductDetailView.as_view()),
    path("manage/", ProductManageView.as_view()),
]
