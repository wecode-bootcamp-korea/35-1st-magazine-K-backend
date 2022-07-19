from django.urls import path

from products.views import ProductView

urlpatterns = [
    path('/product', ProductView.as_view())
]