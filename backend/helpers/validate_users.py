from .shared.common_validations import validate_empty, validate_format_name, validate_email
from django.contrib.auth.models import User
from jose import jwt
from django.conf import settings
from datetime import datetime, timedelta
import uuid
import os
import time
from interfaces.user_interface import Token_payload, Defined_token
from interfaces.shared.responses import Response, ResponseToken

messages = {
    'name': 'The name is required',
    'name_duplicated': 'The user is not available',
    'invalid_name': 'invalid name',
    'email': 'The email is required',
    'invalid_email': 'invalid email',
    'contact_duplicated': 'The contact is not available',
    'password': 'The name is required',
    'password_invalid': 'invalid password',
}

def validate_name(name):
    if validate_empty(name):
        return { 'status': True, 'message': messages['name'] }
    return (
        { 'status': True, 'message': messages['invalid_name'] }
        if not validate_format_name(name)
        else { 'status': False, 'message': '' }   
    )

def validate_user_mail(value):
    if validate_empty(value):
        return { 'status': True, 'message': messages['email'] }
    if not validate_email(value):
        return { 'status': True, 'message': messages['invalid_email'] }
    return (
        { 'status': True, 'message': messages['contact_duplicated'] }
        if User.objects.filter(email=value).exists()
        else { 'status': False, 'message': '' }
    )

def validate_password(value):
    if validate_empty(value):
        return { 'status': True, 'message': messages['password'] }
    return (
        { 'status': True, 'message': messages['password_invalid'] }
        if len(value) < 4
        else { 'status': False, 'message': '' }
    )

def validate_fields_create(name, email, password, **rest) -> Response:
    name_validation = validate_name(name)
    email_validation = validate_user_mail(email)
    password_validation = validate_password(password)
    if name_validation['status'] == True:
        return name_validation
    elif email_validation['status'] == True:
        return email_validation
    return password_validation

def define_token() -> Defined_token:
    token = uuid.uuid4()
    return {
        'token': token,
        'url': f'{os.getenv('BASE_URL')}api/v1/users/verify/{token}'
    }

def get_token(header) -> Token_payload:
    auth = header.split(' ')
    return jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS512'])

def verify_token(header:str) -> bool:
    try:
        if validate_empty(header):
            return False
        result = get_token(header)
        return not int(result['exp']) < int(time.time()) and User.objects.filter(pk=result['id']).get().is_active
    except Exception as err:
        print(err)
        return False

def create_token(user: User) -> ResponseToken:
    try:
        date = datetime.now()
        after = date + timedelta(days=1) # sum 1 day
        format_date = int(datetime.timestamp(after))
        payload = {
            'id': user.pk,
            'ISS': os.getenv('BASE_URL'), # app base domain
            'iat': int(time.time()),
            'exp': format_date
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
        return {
            'status': True,
            'message': f'welcome {user.first_name} {user.last_name}',
            'token': token
        }
    except Exception as err:
        return { 'status': False, 'message': 'Login Failed', 'token': '' }