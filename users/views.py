import json
import re

import bcrypt
import jwt
from django.core.exceptions import ValidationError
from django.conf            import settings
from django.views           import View
from django.http            import JsonResponse

from users.models           import User
from core.utils.validatior  import validator_user_name, validator_email, validator_password

class JoinView(View):

    def post(self, request): 
        try: 
            data = json.loads(request.body)

            username     = data['username']
            password     = data['password']
            name         = data['name']
            phone_number = data['phone_number']
            email        = data['email']

            validator_user_name(username)
            validator_email(email)
            validator_password(password)

            if User.objects.filter(username = username).exists():
                return JsonResponse({'MESSAGE':'Already_Registered_User'}, status=400) 

            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                username     = username,
                password     = hash_password,
                name         = name,
                phone_number = phone_number,
                email        = email,
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        
        except ValidationError as error:
            return JsonResponse({'MESSAGE':error.message}, status = 400)

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSONDecodeError'}, status=400)           

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data['username']
            password = data['password']

            user = User.objects.get(username = username)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
        
            access_token = jwt.encode({'ID': user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'MESSAGE':'SUCCESS', 'AUTHORIZATION':access_token}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)        
