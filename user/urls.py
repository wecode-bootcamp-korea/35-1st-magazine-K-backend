from django.urls import path

from user.views import signup, signin

urlpatterns = [
    path("signup/", signup),
    path("signin/", signin),
]
