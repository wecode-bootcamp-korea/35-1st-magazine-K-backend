from django.urls import path

from orders.views import CartView

urlpatterns = [
    path('/cart/<int:product>', CartView.as_view()),
]
