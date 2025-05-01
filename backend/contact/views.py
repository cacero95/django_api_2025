from rest_framework.views import APIView
from django.http import JsonResponse
from http import HTTPStatus
from .models import Contact
from helpers.validate_contacts import validate_fields_create
from datetime import datetime
from utils.email_actions import send_email

# Create your views here.
class Contacts(APIView):
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
