from django.urls import path, include

urlpatterns = [
    path("api/", include("product.urls")),
    path("api/", include("order.urls")),
    path("api/", include("user.urls")),
    path("api/", include("review.urls")),
]
