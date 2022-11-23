from rest_framework import status


class CustomBaseExecption(Exception):
    is_custom_execption = True


class KeyError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Invaild key. Check the key"
        self.status = status.HTTP_400_BAD_REQUEST


class DuplicateError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Contains data that does not allow duplication. Please check request"
        self.status = status.HTTP_400_BAD_REQUEST


"""
인증 관련 예외처리
"""


class InvaildPayloadError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Invaild payload. Please check token or signin again"
        self.status = status.HTTP_400_BAD_REQUEST


class NotFoundUserError(CustomBaseExecption):
    def __init__(self):
        self.msg = "User not found. Please check email"
        self.status = status.HTTP_400_BAD_REQUEST


class IncorrectPasswordError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Password is worng. Please check password"
        self.status = status.HTTP_400_BAD_REQUEST


class NotAuthorizedError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Login required"
        self.status = status.HTTP_403_FORBIDDEN


class NoPermssionError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Unauthorized request. Please check your permission"
        self.status = status.HTTP_401_UNAUTHORIZED


class TokenExpiredError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Login time expired. Please login again"
        self.status = status.HTTP_403_FORBIDDEN


class EmailValidateError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Email not vaild. Please check email"
        self.status = status.HTTP_400_BAD_REQUEST


class PasswordValidateError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Password not vaild. Please check email"
        self.status = status.HTTP_400_BAD_REQUEST


"""
상품 관련 예외처리
"""


class NotFoundProductError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Product not found. Please check product_id"
        self.status = status.HTTP_400_BAD_REQUEST
