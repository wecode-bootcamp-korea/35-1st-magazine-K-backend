import jwt

from user.models import User
from user.utils.auth_provider import AuthProvider
from .exceptions import NotFoundUserError, InvaildPayloadError, KeyError

auth_provider = AuthProvider()


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = auth_provider.get_token_from_request(request=request)
            user = auth_provider.check_auth(token=token)
            request.user = user
            return func(self, request, *args, **kwargs)
        except User.DoesNotExist:
            raise NotFoundUserError
        except jwt.exceptions.DecodeError:
            return InvaildPayloadError
        except KeyError:
            raise KeyError

    return wrapper
