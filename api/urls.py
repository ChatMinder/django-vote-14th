from django.urls import path
from rest_framework import urlpatterns
from api.views import AuthCookieView, AuthViewHttpOnly, UserDetailView, UserDuplicateView, UserView, AuthView 

urlpatterns = [
    path('users', UserView.as_view()),
    path('users/<int:pk>', UserDetailView.as_view()),
    path('users/duplicate', UserDuplicateView.as_view()),
    path('auth/token', AuthView.as_view()),
    path('auth/token/cookie', AuthCookieView.as_view()),
    path('auth/token/cookie/only', AuthViewHttpOnly.as_view())
]