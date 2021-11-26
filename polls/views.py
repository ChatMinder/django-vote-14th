from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from polls.models import *
from polls.serializers import QuestionSerializer, CandidateSerializer, VoteSerializer
from rest_framework.views import APIView
from api.models import User


def get_user(self, pk):
    return get_object_or_404(User, pk=pk)


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class CandidateViewSet(ModelViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()


class CastVote(APIView):
    def post(self, request, pk):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            created_instance = serializer.create(validated_data=request.data)
            created_instance.user_id = self.get_user(pk)

            try:
                created_instance.save()

            except IntegrityError:
                return Response(
                    {
                        "message": "Already voted"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {
                    "message": "Vote cast successful"
                },
                status=status.HTTP_200_OK
            )
