from django.urls    import path

from products.views import ProductDetailView, ProductView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]
