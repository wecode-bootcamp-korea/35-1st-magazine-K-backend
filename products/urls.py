from django.urls    import path

from products.views import ProductDetailView

from products.views import ProductView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]
