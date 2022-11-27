from rest_framework import status
from rest_framework.exceptions import APIException

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    return response


class KeyError(APIException):
    default_detail = "Invaild key. Check the key"
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "invaild_key"


class DuplicateError(APIException):
    default_detail = "Contains data that does not allow duplication. Please check request"
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "not_allow_dupilcate"


"""
인증 관련 예외처리
"""


class InvaildPayloadError(APIException):
    default_detail = "Invaild payload. Please check token or signin again"
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "invaild_payload"


class NotFoundUserError(APIException):
    default_detail = "User not found. Please check email"
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "user_not_found"


class IncorrectPasswordError(APIException):
    default_detail = "Password is worng. Please check password"
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "password_is_worng"


class NotAuthorizedError(APIException):
    default_detail = "Login required"
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "login_required"


class NoPermssionError(APIException):
    default_detail = "Unauthorized request. Please check your permission"
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "unauthorized_request"


class TokenExpiredError(APIException):
    default_detail = "Login time expired. Please login again"
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "login_time_expired"


class EmailValidateError(APIException):
    default_detail = "Email not vaild. Please check email"
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "email_not_vaild"


class PasswordValidateError(APIException):
    default_detail = "Password not vaild. Please check email"
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "password_not_vaild"


"""
상품 관련 예외처리
"""


class NotFoundProductError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Product not found. Please check product_id"
    default_code = "product_not_found"


"""
장바구니 관련 예외처리
"""


class OutOfRangeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The number of products cannot be less than one. Please check number"
    default_code = "out_of_range"


"""
리뷰 관련 예외처리
"""


class NotFoundReviewError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Review not found. Please check review_id"
    default_code = "review_not_found"


class NotPurchasedError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = (
        "Do not have permission to create a review. Please check user purchased the product"
    )
    default_code = "not_permission"


class AlreadyExistError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The review user wrote exists. Please check"
    default_code = "already_exist"


class NotAuthorizationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "This review was not written by this user. Please check user_id"
    default_code = "not_permission"
