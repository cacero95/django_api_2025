from django.urls import path
from .views import home_init

urlpatterns = [
    path('', home_init)
]