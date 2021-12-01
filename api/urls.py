from django.urls import path
from rest_framework import urlpatterns
from api.views import AuthView, AuthViewHttpOnly, UserDetailView, UserDuplicateView, UserView 

urlpatterns = [
    path('users', UserView.as_view()),
    path('users/<int:pk>', UserDetailView.as_view()),
    path('users/duplicate', UserDuplicateView.as_view()),
    path('auth/token', AuthView.as_view()),
    path('auth/token/only', AuthViewHttpOnly.as_view())
]