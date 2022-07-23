from django.urls import path

from products.views import ProductView

urlpatterns = [
    path('/list', ProductView.as_view())
]
