from rest_framework import serializers

from .models import User


class SignupReq(serializers.Serializer):
    """
    회원가입 요청 값 직렬화
    """

    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=16)
    name = serializers.CharField(max_length=20)
    phone_number = serializers.CharField(max_length=50)


class SigninReq(serializers.Serializer):
    """
    로그인 요청 값 직렬화
    """

    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=16)


class UserRepo:
    def __init__(self) -> None:
        self.DEFAULT_POINT = 100000

    def create_user(
        self,
        email: str,
        password: str,
        name: str,
        phone_number: str,
    ) -> bool:
        User.objects.create(
            email=email,
            password=password,
            name=name,
            phone_number=phone_number,
            point=self.DEFAULT_POINT,
        )
        return True

    def get_user_by_email(self, email: str) -> object:
        return User.objects.get(email=email)
