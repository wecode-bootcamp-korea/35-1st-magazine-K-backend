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


@api_view(["POST"])
def signout(request):
    token = auth_provider.get_token_from_request(request=request)
    expired_token = auth_provider.signout(token=token)
    return JsonResponse({"expired_token": expired_token, "status": status.HTTP_200_OK})
