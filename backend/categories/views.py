from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from http import HTTPStatus
from .models import Category
from .serializers import CategorySerializer
from django.utils.text import slugify
from recipe.models import Recipe
from security.decorators import with_token, with_token2
from helpers.validate_category import validate_fields_create
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

def my_decorator(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print("Custom decorator called")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

class Categories(APIView):
    @swagger_auto_schema(
        operation_description = 'create a new user',
        responses = {
            200: 'Success',
            401: 'Unauthorized'
        },
        security=[{'Token': []}]
    )
    @method_decorator([with_token2])
    def get(self, request):
        data = Category.objects.order_by('-id').all()
        data_json = CategorySerializer(data, many=True)
        return JsonResponse({
            'status': 'ok',
            'data': data_json.data
        }, status=HTTPStatus.OK)
    
    @with_token()
    def post(self, request):
        try:
            status, message = validate_fields_create(request.data['name']).values()
            if status:
                return JsonResponse({
                    'status': False,
                    'message': message
                }, status=HTTPStatus.BAD_REQUEST)

            Category.objects.create(name=request.data['name'])
            return JsonResponse({
                'status': True,
                'message': 'created'
            }, status=HTTPStatus.CREATED)
        except Exception as err:
            print(type(err))
            return JsonResponse({
                'status': False,
                'message': f'These fields are required {err}'
            }, status=HTTPStatus.BAD_REQUEST)

    
class CategoriesByParam(APIView):
    def get(self, request, id):
        # (pk = id) === (id = id)
        try:
            data = Category.objects.filter(id=id).get()
            return JsonResponse({
                'status': 'ok',
                'data': {
                    'name': data.name,
                    'slug': data.slug
                }
            }, status=HTTPStatus.OK)
        except Category.DoesNotExist:
            raise Http404
        
    @with_token()
    def put(self, request, id):
        try:
            if request.data.get('name') == None or not request.data['name']:
                return JsonResponse({
                    'status': False,
                    'message': 'The field name is required'
                }, status=HTTPStatus.BAD_REQUEST)
            name = request.data['name']
            Category.objects.filter(pk=id).update(name=name, slug=slugify(name))
            return JsonResponse({
                'status': 'ok',
                'message': 'updated'
            }, status=HTTPStatus.OK)
        except Category.DoesNotExist:
            raise Http404
        
    @with_token()    
    def delete(self, request, id):
        try:
            category = Category.objects.filter(pk=id).get()
            if not Recipe.objects.filter(pk=id).exists():
                category.delete()
                return JsonResponse({
                    'status': True,
                    'message': 'Deleted'
                }, HTTPStatus.OK)
            return JsonResponse({
                'status': False,
                'message': 'unexpected error'
            }, status=HTTPStatus.BAD_REQUEST)
        except Category.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': f'Not found'
            }, status=HTTPStatus.NOT_FOUND)

