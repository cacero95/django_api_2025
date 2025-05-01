from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from http import HTTPStatus
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime

class Class_Example(APIView):
    def get(self, request):
        return JsonResponse({
            'status': 'ok',
            'message': f'Hello GET {request.GET.get('id', '')}'
        }, status=HTTPStatus.OK)
    def post(self, request):
        # get the body at the request
        mail = request.data.get('mail')
        password = request.data.get('password')
        if mail == None or password == None:
            return JsonResponse({
                'status': 'False',
                'message': 'Es requerido el mail y el password'
            }, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({
            'status': 'ok',
            'message': f'created'
        }, status=HTTPStatus.CREATED)
    def patch(self, request):
        return HttpResponse('<h1>Hello PATCH</h1>')

class UrlParams(APIView):
    def get(self, request, id):
        return HttpResponse(f'<h1>Hello GET {id}</h1>')
    def put(self, request, id):
        return HttpResponse(f'<h1>Hello PUT {id}</h1>')
    def delete(self, request):
        return HttpResponse(f'<h1>Hello DELETE {id}</h1>')
    
class FileClass(APIView):
    def patch(self, request):
        try:
            fs = FileSystemStorage()
            date = datetime.now()
            # concat the date now with the format of the image
            image = f'{datetime.timestamp(date)}{os.path.splitext(str(request.FILES['file']))[1]}'
            fs.save(f'example/{image}', request.FILES['file'])
            return JsonResponse({
                'status': 'ok',
                'message': 'saved'
            }, status=HTTPStatus.ACCEPTED)
        except Exception as error:
            return JsonResponse({
                'status': False,
                'message': error
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)