from rest_framework import status


class CustomBaseExecption(Exception):
    is_custom_execption = True


class KeyError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Invaild key. Check the key"
        self.status = status.HTTP_400_BAD_REQUEST


class NoPurchasedError(CustomBaseExecption):
    def __init__(self):
        self.msg = "User who did not purchase the product."
        self.status = status.HTTP_400_BAD_REQUEST


class AlreadyExistError(CustomBaseExecption):
    def __init__(self):
        self.msg = "A review already created exists."
        self.status = status.HTTP_400_BAD_REQUEST


class NotExistError(CustomBaseExecption):
    def __init__(self):
        self.msg = "A review not exists."
        self.status = status.HTTP_400_BAD_REQUEST


class NotAuthorizationError(CustomBaseExecption):
    def __init__(self):
        self.msg = "User does not have permission."
        self.status = status.HTTP_401_UNAUTHORIZED
