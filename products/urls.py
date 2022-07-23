from django.urls    import path

from products.views import ProductDetailView

urlpatterns = [
    path('/<int:category_id>/<int:product_id>', ProductDetailView.as_view()),
]
