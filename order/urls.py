from django.urls import path

from order.views import CartAPI, OrderAPI, OrderStatusAPI

urlpatterns = [
    path("cart/", CartAPI.as_view()),
    path("cart/<int:product_id>/", CartAPI.as_view()),
    path("cart/<int:product_id>/<str:calculation>/", CartAPI.as_view()),
    path("order/", OrderAPI.as_view()),
    path("order/status/", OrderStatusAPI.as_view()),
]
