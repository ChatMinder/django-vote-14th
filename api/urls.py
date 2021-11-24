from django.urls import path
from rest_framework import urlpatterns

from api.views import UserView 

urlpatterns = [
    path('users', UserView.as_view()),
]