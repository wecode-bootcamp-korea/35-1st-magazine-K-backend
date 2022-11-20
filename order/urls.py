from django.urls import path

from order.views import CartAPI, OrderStatusAPI

urlpatterns = [
    path("cart/", CartAPI.as_view()),
    path("order/status/", OrderStatusAPI.as_view()),
]
