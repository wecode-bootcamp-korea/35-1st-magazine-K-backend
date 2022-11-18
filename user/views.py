from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse

from .serializers import SignupReq, SigninReq
from .utils.auth_provider import AuthProvider

auth_provider = AuthProvider()


@api_view(["POST"])
def signup(request):
    params = request.data
    serializer = SignupReq(data=params)
    serializer.is_valid()
    auth_provider.signup(**serializer.data)
    return JsonResponse({"status": status.HTTP_201_CREATED})


@api_view(["POST"])
def signin(request):
    params = request.data
    serializer = SigninReq(data=params)
    serializer.is_valid()
    token = auth_provider.signin(**serializer.data)
    return JsonResponse({"access_token": token, "status": status.HTTP_200_OK})
