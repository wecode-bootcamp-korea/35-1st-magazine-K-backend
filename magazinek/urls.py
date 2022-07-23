from django.urls import path, include

urlpatterns = [
    path('products', include('products.urls')),
    path('orders', include('orders.urls')),
    path('users', include('users.urls')),
]
