from django.urls import path
from .views import Recipes, RecipesByParam

urlpatterns = [
    path('recipes', Recipes.as_view()),
    path('recipes/<int:id>', RecipesByParam.as_view()),
]