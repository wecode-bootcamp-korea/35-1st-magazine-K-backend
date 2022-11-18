from django.urls import path

from user.views import signup

urlpatterns = [
    path("signup/", signup),
]
