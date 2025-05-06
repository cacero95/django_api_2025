from rest_framework.views import APIView
from django.http import JsonResponse
from http import HTTPStatus
from .models import Contact
from helpers.validate_contacts import validate_fields_create
from datetime import datetime
from utils.email_actions import send_email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class Contacts(APIView):
    @swagger_auto_schema(
        operation_description = 'Endpoint create a new contact',
        responses = {
            200: 'Success',
            400: 'Bad request'
        },
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                'name': openapi.Schema( type = openapi.TYPE_STRING ),
                'email': openapi.Schema( type = openapi.TYPE_STRING ),
                'phone': openapi.Schema( type = openapi.TYPE_STRING ),
                'message': openapi.Schema( type = openapi.TYPE_STRING, description = 'message to the new contact' ),
            },
            required = ['name', 'email', 'phone', 'message']
        )
    )
    def post(self, request):
        status, message = validate_fields_create(**request.data).values()
        if status:
            return JsonResponse({
                'status': False,
                'message': message
            }, status=HTTPStatus.BAD_REQUEST)
        Contact.objects.create(
            name=request.data['name'],
            email=request.data['email'],
            phone=request.data['phone'],
            message=request.data['message'],
            created_date=datetime.now(),
            update_date=datetime.now()
        )
        html = f"""
            <h1>New record</h1>
            <ul>
                <li>name: {request.data['name']}</li>
                <li>email: {request.data['email']}</li>
                <li>phone: {request.data['phone']}</li>
                <li>message: {request.data['message']}</li>
            </ul>
        """
        send_email(html, 'testing', request.data['email'])
        try:
            return JsonResponse({
                'status': True,
                'message': 'created'
            }, status=HTTPStatus.OK)
        except Exception as err:
            return JsonResponse({
                'status': False,
                'message': f'{err}'
            }, status=HTTPStatus.BAD_REQUEST)
