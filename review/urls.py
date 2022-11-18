from django.urls import path

from review.views import ReviewView

urlpatterns = [
    path("<int:product_id>/reviews/", ReviewView.as_view()),
    path("<int:product_id>/reviews/<int:review_id>/", ReviewView.as_view()),
]
