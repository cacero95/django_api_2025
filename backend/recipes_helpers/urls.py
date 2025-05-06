from django.urls import path
from .views import UserRecipe, UpdateUserRecipeByID, RecipeBySlug, RecipesHome

urlpatterns = [
    path('user_recipe', UserRecipe.as_view()),
    path('user_recipe/update/image/<int:id>', UpdateUserRecipeByID.as_view()),
    path('user_recipe/slug/<str:slug>', RecipeBySlug.as_view()),
    path('user_recipe/home/recipes', RecipesHome.as_view())
]