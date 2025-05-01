from django.urls import path
from .views import Categories, CategoriesByParam

urlpatterns = [
    path('categories', Categories.as_view()),
    path('categories/<int:id>', CategoriesByParam.as_view()),
]