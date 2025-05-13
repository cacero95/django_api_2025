from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from http import HTTPStatus
from helpers.validate_users import validate_fields_create, define_token, create_token
from django.contrib.auth.models import User
from helpers.shared.common_validations import validate_empty
from .models import UserMetaData
from utils.email_actions import send_email
import os
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class Security(APIView):
    @swagger_auto_schema(
        operation_description = 'create a new user',
        responses = {
            200: 'Success',
            400: 'Bad request'
        },
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                'name': openapi.Schema( type = openapi.TYPE_STRING ),
                'email': openapi.Schema( type = openapi.FORMAT_EMAIL ),
                'password': openapi.Schema( type = openapi.FORMAT_PASSWORD ),
            },
            required = ['name', 'email', 'password']
        )
    )
    def post(self, request):
        try:
            status, message = validate_fields_create(**request.data).values()
            last_name = request.data['last_name'] if not validate_empty(request.data['last_name']) else ''
            if status:
                return JsonResponse({
                    'status': False,
                    'message': message
                }, status=HTTPStatus.BAD_REQUEST)
            email = request.data['email']
            user = User.objects.create_user(
                username=email,
                email=email,
                password=request.data['password'],
                first_name=request.data['name'],
                last_name=last_name,
                is_active=0
            )
            token, url = define_token().values()
            UserMetaData.objects.create(token=token, user_id=user.pk)
            html = f"""
                <h1>account verification</h1>
                <p>For verify the account please enter to the next link: <a href="{url}">{url}</a></p>
            """
            send_email(html, 'new user', email)
            return JsonResponse({
                'status': True,
                'message': 'created'
            }, status=HTTPStatus.CREATED)
        except Exception as err:
            return JsonResponse({
                'status': False,
                'message': f'{err}'
            }, status=HTTPStatus.BAD_REQUEST)

class VerifyUser(APIView):
    def get(self, request, token):
        print(token)
        if validate_empty(token):
            return JsonResponse({
                'status': False,
                'message': 'Not found'
            }, status=HTTPStatus.NOT_FOUND)
        try:
            # the __ indicate to the django ORM to look for by a foreign field
            user = UserMetaData.objects.filter(token=token).filter(user__is_active=0).get()
            UserMetaData.objects.filter(token=token).update(token='')
            User.objects.filter(id=user.user_id).update(is_active=1)
            return HttpResponseRedirect(os.getenv('BASE_URL_FRONTEND'))
        except UserMetaData.DoesNotExist:
            return JsonResponse({
                'status': True,
                'message': 'Not found'
            }, status=HTTPStatus.NOT_FOUND)
        
class LoginUser(APIView):
    @swagger_auto_schema(
        operation_description = 'Login',
        responses = {
            200: 'Success',
            400: 'Bad request'
        },
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                'email': openapi.Schema( type = openapi.FORMAT_EMAIL ),
                'password': openapi.Schema( type = openapi.FORMAT_PASSWORD ),
            },
            required = ['email', 'password']
        )
    )
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if validate_empty(email) or validate_empty(password):
            return JsonResponse({
                'status': False,
                'message': 'bad request'
            }, status=HTTPStatus.BAD_REQUEST)
        try:
            user = User.objects.filter(email=email).get()
            if authenticate(request, username=email, password=password) == None:
                return JsonResponse({
                    'status': False,
                    'message': 'unauthorized'
                }, status=HTTPStatus.UNAUTHORIZED)
            status, message, token, username, name = create_token(user).values()
            status_code = HTTPStatus.OK if status else HTTPStatus.BAD_REQUEST
            return JsonResponse({
                'status': status,
                'message': message,
                'token': token,
                'username': username,
                'name': name
            }, status=status_code)
        except User.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'Not found'
            }, status=HTTPStatus.NOT_FOUND)