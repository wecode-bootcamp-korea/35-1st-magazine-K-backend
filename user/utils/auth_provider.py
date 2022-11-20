from datetime import datetime
import bcrypt
import jwt
import re

from django.conf import settings
from django.core.exceptions import ValidationError

from ..serializers import UserRepo
from core.utils.exceptions import (
    NotFoundError,
    NotFoundUserError,
    NotAuthorizedError,
    TokenExpiredError,
)


class AuthProvider:
    def __init__(self):
        self.key = settings.SECRET_KEY
        self.expire_sec = settings.JWT_EXPIRE_TIME
        self.user_repo = UserRepo()

    def _get_curr_sec(self):
        return datetime.now().timestamp()

    def hashpw(self, password: str):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    def checkpw(self, password: str, hashed: str):
        return bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8"))

    def _decode(self, token: str):
        decoded = jwt.decode(token, self.key, algorithms=["HS256"])
        if decoded["exp"] <= self._get_curr_sec():
            raise TokenExpiredError
        else:
            return decoded

    def get_token_from_request(self, request):
        return request.META.get("HTTP_AUTHORIZATION", None)

    def create_token(self, user_id: str, is_expired: bool = False):
        exp = 0 if is_expired else self._get_curr_sec() + self.expire_sec
        encoded_jwt = jwt.encode(
            {"id": user_id, "exp": exp},
            self.key,
            algorithm="HS256",
        )
        return encoded_jwt

    def validate_email(self, email):
        REGEX_EMAIL = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(REGEX_EMAIL, email):
            raise ValidationError("Invalid Email format")

    def validate_password(self, password):
        REGEX_PASSWORD = (
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%^&*()])[A-Za-z\d~!@#$%^&*()]{8,16}"
        )
        if not re.match(REGEX_PASSWORD, password):
            raise ValidationError("Invalid password format")

    def signup(
        self,
        email: str,
        password: str,
        name: str,
        phone_number: str,
    ) -> bool:
        self.validate_email(email=email)
        self.validate_password(password=password)
        hashpw = self.hashpw(password=password)
        self.user_repo.create_user(
            email=email,
            password=hashpw,
            name=name,
            phone_number=phone_number,
        )
        return True

    def signin(self, email: str, password: str):
        try:
            user = self.user_repo.get_user_by_email(email=email)
            if self.checkpw(password, user["password"]):
                return self.create_token(user["id"])
            else:
                raise NotFoundUserError()
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise NotFoundUserError()
            else:
                raise e

    def signout(self, token: str):
        decoded = self._decode(token)
        return self.create_token(decoded["id"], is_expired=True)

    def check_auth(self, token: str) -> bool:
        decoded = self._decode(token)
        try:
            user = self.user_repo.get_user_by_id(decoded["id"])
            if user:
                return user
            else:
                raise NotAuthorizedError
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise NotAuthorizedError
