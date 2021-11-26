from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from polls.serializers import QuestionSerializer


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question
