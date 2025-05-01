from django.urls import path
from .views import UserRecipe, UserRecipeByID

urlpatterns = [
    path('user_recipe', UserRecipe.as_view()),
    path('user_recipe/update/image/<int:id>', UserRecipeByID.as_view()),
]