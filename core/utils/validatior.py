import re

from django.core.exceptions import ValidationError

def validator_user_name(user_name):
    REGEX_USER_NAME = '^[a-zA-Z0-9]{4,16}$'
    if not re.match(REGEX_USER_NAME, user_name):
        raise ValidationError('Invalid Id format')

def validator_email(email):
    REGEX_EMAIL  = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(REGEX_EMAIL, email):
        raise ValidationError('Invalid Email format')

def validator_password(password):
    REGEX_PASSWORD = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%^&*()])[A-Za-z\d~!@#$%^&*()]{8,16}'
    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError('Invalid password format')