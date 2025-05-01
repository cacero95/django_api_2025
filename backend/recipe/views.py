from rest_framework.views import APIView
from django.http import JsonResponse
from http import HTTPStatus
from django.utils.text import slugify
from .models import Recipe
from .serializers import RecipeSerializer
from django.utils.dateformat import DateFormat
from helpers.validate_image import format_image
from helpers.validate_users import get_token
from helpers.validate_recipes import validate_fields_create, save_file, validate_update_recipe, validate_category
import os
from security.decorators import with_token

class Recipes(APIView):
    def get(self, request):
        data = Recipe.objects.order_by('-id').all()
        return JsonResponse({
            'status': 'ok',
            'data': RecipeSerializer(data, many=True).data
        }, status=HTTPStatus.OK)
    
    @with_token()
    def post(self, request):
        try:
            status, message = validate_fields_create(**request.data).values()
            file_validation = save_file(request.FILES['image'])
            if status:
                return JsonResponse({
                    'status': False,
                    'message': message
                }, status=HTTPStatus.BAD_REQUEST)
            elif file_validation['status'] == False:
                return JsonResponse({
                    'status': False,
                    'message': file_validation['message']
                }, status=HTTPStatus.BAD_REQUEST)
            token = get_token(request.headers.get('Authorization'))
            Recipe.objects.create(
                name=request.data['name'],
                user_id=token['id'],
                description=request.data['description'],
                time=request.data['time'],
                category_id=request.data['category'],
                image=file_validation['path']
            )
            return JsonResponse({
                'status': 'ok',
                'message': 'created'
            }, status=HTTPStatus.CREATED)
        except Exception as err:
            return JsonResponse({
                'status': False,
                'message': f'{err}'
            }, status=HTTPStatus.BAD_REQUEST)
        
class RecipesByParam(APIView):
    def get(self, request, id):
        try:
            data = Recipe.objects.filter(pk=id).get()
            return JsonResponse({
                'status': 'ok',
                'data': {
                    'name': data.name,
                    'description': data.description,
                    'time': data.time,
                    'image': format_image(data.image),
                    'created_date': DateFormat(data.created_date).format('d/m/Y'),
                    'category': data.category.name,
                    'category_id': data.category_id
                }
            }, status=HTTPStatus.OK)
        except Recipe.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': f'Not found'
            }, status=HTTPStatus.NOT_FOUND)
    
    @with_token()
    def put(self, request, id):
        try:
            recipe = Recipe.objects.filter(pk=id)
            if recipe.exists():
                actual_recipe = recipe.get()
                status, path, message = save_file(request.FILES['image']).values()
                if not status:
                    return JsonResponse({
                        'status': False,
                        'message': message
                    }, status=HTTPStatus.BAD_REQUEST)
                else:
                    response_path = path if path else actual_recipe.image
                    update_data = validate_update_recipe(
                        { **request.data, 'image': response_path },
                        actual_recipe
                    )
                    category = validate_category( update_data['category'][0] )
                    if category['status']:
                        return JsonResponse({
                            'status': False,
                            'message': category['message']
                        }, status=HTTPStatus.BAD_REQUEST)
                    recipe.update(
                        name = update_data['name'][0],
                        slug = slugify(update_data['name'][0]),
                        time = update_data['time'][0],
                        image = update_data['image'],
                        description = update_data['description'][0],
                        category = update_data['category'][0]
                    )
                    return JsonResponse({
                        'status': True,
                        'message': 'updated'
                    }, status=HTTPStatus.OK)
        except Exception as error:
            return JsonResponse({
                'status': False,
                'message': f'{error}'
            }, status=HTTPStatus.NOT_FOUND)
        
    @with_token()
    def delete(self, request, id):
        try:
            recipe = Recipe.objects.filter(pk=id)
            record = recipe.get()
            os.remove(f'./files/recipe/{record.image}')
            recipe.delete()
            return JsonResponse({
                'status': 'ok',
                'message': 'deleted'
            }, status=HTTPStatus.OK)
        except Recipe.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': f'Not found'
            }, status=HTTPStatus.NOT_FOUND)