from functools import wraps
from helpers.validate_users import verify_token
from django.http.response import JsonResponse
from http import HTTPStatus


def with_token2(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        # req = args[0]
        auth:str = request.headers.get('Authorization')
        if not verify_token(auth):
            return JsonResponse({
                'status': False,
                'message': 'unauthorized'
            }, status=HTTPStatus.UNAUTHORIZED)
        return func(request, *args, **kwargs)
    return _decorator

def with_token():
    def validate(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            req = args[0]
            auth:str = req.headers.get('Authorization')
            if not verify_token(auth):
                return JsonResponse({
                    'status': False,
                    'message': 'unauthorized'
                }, status=HTTPStatus.UNAUTHORIZED)
            return func(request, *args, **kwargs)
        return _decorator
    return validate