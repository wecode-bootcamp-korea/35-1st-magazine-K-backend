import decimal

from rest_framework import serializers

from core.exceptions import NotFoundUserError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "name", "phone_number", "point"]


class SignupReq(serializers.Serializer):
    """
    회원가입 요청 값 직렬화 클래스
    """

    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=16)
    name = serializers.CharField(max_length=20)
    phone_number = serializers.CharField(max_length=50)


class SigninReq(serializers.Serializer):
    """
    로그인 요청 값 직렬화 클래스
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
        created = User.objects.create(
            email=email,
            password=password,
            name=name,
            phone_number=phone_number,
            point=self.DEFAULT_POINT,
        )
        return UserSerializer(created).data

    def get_user_by_id(self, user_id: int) -> dict:
        try:
            return UserSerializer(User.objects.get(id=user_id)).data
        except User.DoesNotExist:
            raise NotFoundUserError

    def get_user_by_email(self, email: str) -> object:
        try:
            return UserSerializer(User.objects.get(email=email)).data
        except User.DoesNotExist:
            raise NotFoundUserError

    def deduct_user_point(self, user_id: int, total_price: float) -> bool:
        """
        상품 구매 시 회원의 포인트를 차감시키는 함수
        """
        User.objects.filter(id=user_id).update(
            point=User.objects.get(id=user_id).point - decimal.Decimal(total_price),
        )
        return True
