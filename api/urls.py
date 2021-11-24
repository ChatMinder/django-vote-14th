from django.urls import path
from rest_framework import urlpatterns
from api.views import AuthView, UserView 

urlpatterns = [
    path('users', UserView.as_view()),
    path('auth/token', AuthView.as_view()),
]