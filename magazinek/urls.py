from django.urls import path, include

urlpatterns = [
    path('products', include('products.urls')),
    path('member', include('users.urls')),
]
