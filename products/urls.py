from django.urls import path

from products.views import ProductView, ProductDetailView, SearchView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/search/<str:keyword>', SearchView.as_view())
]
