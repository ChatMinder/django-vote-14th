
from rest_framework.viewsets import ModelViewSet
from polls.models import *
from polls.serializers import QuestionSerializer


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
