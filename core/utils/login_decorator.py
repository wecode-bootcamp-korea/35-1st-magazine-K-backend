import json

import jwt
from django.conf  import settings
from django.http  import JsonResponse

from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:       
            access_token = request.headers.get('Authorization')           
            payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, stauts=401)

        except jwt.excetions.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_PAYLOAD'}, stauts=401) 

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)           
    
    return wrapper      