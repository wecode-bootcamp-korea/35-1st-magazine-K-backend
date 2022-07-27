from django.urls import path

from orders.views import CartView, OrderView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/cart/<int:product_id>', CartView.as_view()),
    path('', OrderView.as_view())
]
