from django.shortcuts import render
from rest_framework.views import APIView
from security.decorators import with_token
from helpers.validate_users import get_token
from django.http import JsonResponse
from http import HTTPStatus
from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from helpers.validate_recipes import save_file

class UserRecipe(APIView):
    @with_token()
    def get(self, request):
        try:
            token = get_token(request.headers.get('Authorization'))
            data = Recipe.objects.filter(user_id=token['id']).order_by('-id').all()
            return JsonResponse({
                'status': True,
                'message': 'success',
                'data': RecipeSerializer(data, many=True).data
            }, status=HTTPStatus.OK)
        except Exception as err:
            return JsonResponse({
                'status': False,
                'message': f'{err}'
            }, status=HTTPStatus.BAD_REQUEST)
        
class UserRecipeByID(APIView):
    @with_token()
    def put(self, request, id):
        try:
            token = get_token(request.headers.get('Authorization'))
            recipe = Recipe.objects.filter(pk=id, user_id=token['id'])
            item = recipe.get()
            status, path, message = save_file(request.FILES['image'], item.image).values()
            if not status:
                return JsonResponse({
                    'status': False,
                    'message': message
                }, status=HTTPStatus.BAD_REQUEST)
            recipe.update(image=path)
            return JsonResponse({
                'status': True,
                'message': 'ok'
            }, status=HTTPStatus.OK)
        except Recipe.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'not found'
            }, status=HTTPStatus.NOT_FOUND)