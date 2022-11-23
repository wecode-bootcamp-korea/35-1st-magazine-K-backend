from rest_framework import status


class CustomBaseExecption(Exception):
    is_custom_execption = True


class KeyError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Invaild Key. Check the key"
        self.status = status.HTTP_400_BAD_REQUEST


class InvaildPayloadError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Invaild Payload. Please Check Token or Signin Again"
        self.status = status.HTTP_400_BAD_REQUEST


class NotFoundError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Data Not Found. Please Check ID"
        self.status = status.HTTP_400_BAD_REQUEST


class NotFoundUserError(CustomBaseExecption):
    def __init__(self):
        self.msg = "User Not Found. Please Check ID or Password"
        self.status = status.HTTP_400_BAD_REQUEST


class NotAuthorizedError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Login Required"
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
