from django.urls import path
from rest_framework import urlpatterns

from api.views import HelloView

urlpatterns = [
    path('hello', HelloView.as_view()),
]