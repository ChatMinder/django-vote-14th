from django.urls import path
from django.urls.conf import include
from rest_framework import urlpatterns
from api.views import AuthCookieView, AuthViewHttpOnly, UserDetailView, UserDuplicateView, UserView, AuthView 
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users', UserView.as_view()),
    path('users/<int:pk>', UserDetailView.as_view()),
    path('users/duplicate', UserDuplicateView.as_view()),
    path('auth/token', AuthView.as_view()),
    path('auth/token/refresh', TokenRefreshView.as_view()),
    path('auth/token/cookie', AuthCookieView.as_view()),
    path('auth/token/cookie/only', AuthViewHttpOnly.as_view()),
    path('polls/', include('polls.urls'))
]