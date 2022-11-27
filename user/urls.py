from django.urls import path

from user.views import signup, signin, signout

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
]
