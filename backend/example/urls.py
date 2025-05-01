from django.urls import path
from .views import Class_Example, UrlParams, FileClass

urlpatterns = [
    path('example', Class_Example.as_view()),
    path('example/<int:id>', UrlParams.as_view()),
    path('example/upload', FileClass.as_view()),
]