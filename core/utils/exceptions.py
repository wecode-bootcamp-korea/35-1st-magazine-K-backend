from rest_framework import status


class CustomBaseExecption(Exception):
    is_custom_execption = True


class NotFoundError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Data Not Found. Please Check ID"


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


class NoResultToRetrieveRowCountError(CustomBaseExecption):
    def __init__(
        self,
        message: str = "no .execute*() has been performed on the cursor or the rowcount of the last operation is cannot be determined by the interface.",
    ):
        self.message = message
        self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

        super(NoResultToRetrieveRowCountError, self).__init__(self.message)


class TooManyCursorResult(CustomBaseExecption):
    def __init__(
        self,
        message: str = "cursor 실행 결과가 예상치를 초과하였습니다.",
    ):
        self.message = message
        self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        super(TooManyCursorResult, self).__init__(self.message)
