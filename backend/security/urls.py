from django.urls import path
from .views import Security, VerifyUser, LoginUser

urlpatterns = [
    path('users', Security.as_view()),
    path('users/verify/<str:token>', VerifyUser.as_view()),
    path('users/login', LoginUser.as_view()),
]