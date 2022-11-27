from django.urls import path

from .views import ReviewAPI

urlpatterns = [
    path("product/<int:product_id>/review/", ReviewAPI.as_view()),
    path("product/review/<int:review_id>/", ReviewAPI.as_view()),
]
