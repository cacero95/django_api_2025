from django.shortcuts import render
from rest_framework.views import APIView
from security.decorators import with_token
from helpers.validate_users import get_token
from django.http import JsonResponse
from http import HTTPStatus
from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from helpers.validate_recipes import save_file
from django.db.models.manager import BaseManager
from typing import Literal

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
        
class UpdateUserRecipeByID(APIView):
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

class RecipeBySlug(APIView):
    @with_token()
    def get(self, request, slug):
        try:
            recipe = Recipe.objects.filter(slug=slug).get()
            return JsonResponse({
                'status': True,
                'data': RecipeSerializer(recipe, many=False).data
            }, status=HTTPStatus.OK)
        except Recipe.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'not found'
            }, status=HTTPStatus.NOT_FOUND)
        
class RecipesHome(APIView):
        
    def get_by_filter(self, recipes: BaseManager[Recipe], search:Literal['all', 'category', 'slug'], value:str):
        try:
            if search == 'category':
                return recipes.filter(category=value).order_by('-id')
            elif search == 'slug':
                #__contains equals to select * from recipes where slug like value
                #__icontains equals to select * from recipes where slug like %value%
                return recipes.filter(slug__icontains=value).order_by('-id')
            return recipes.order_by('-id')
        except:
            return recipes

    def apply_limit(self, recipes: BaseManager[Recipe], limit:int):
        return recipes.all() if limit == 0 else recipes.all()[:limit]

    @with_token()
    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 0))
            search = request.query_params.get('search', 'all')
            value = request.query_params.get('value', '')
            token = get_token(request.headers.get('Authorization'))
            #order_by('?') equals to select * from Recipes order by rand()
            #[:3] equals to select * from Recipes limit 3 -- return the last 3
            recipes = Recipe.objects.filter(user_id=token['id'])
            out = self.get_by_filter(recipes, search, value)
            out = self.apply_limit(out, limit)
            return JsonResponse({
                'status': True,
                'data': RecipeSerializer(out, many=True).data
            }, status=HTTPStatus.OK)
        except Recipe.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'not found'
            }, status=HTTPStatus.NOT_FOUND)
