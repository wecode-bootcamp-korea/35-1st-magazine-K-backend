from django.urls import path, include

urlpatterns = [
    path('products', include('products.urls')),
    path('orders', include('orders.urls')),
    path('member', include('users.urls')),
    path('products', include('reviews.urls')),   
]
