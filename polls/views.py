from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.views import View, generic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from polls.models import *
from polls.serializers import QuestionSerializer, CandidateSerializer, VoteSerializer
from rest_framework.views import APIView
from api.models import User


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class CandidateViewSet(ModelViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()


class CastVote(APIView):
    #authentication_classes = JWTAuthentication

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        user = request.user
        #유저가 인증되지 않았으면 로그인페이지로 이동
        if user.is_authenticated:
            return redirect("/auth/token/")
        else:
            if serializer.is_valid():
                created_instance = serializer.create(validated_data=request.data)
                created_instance.user.id = user.id
                created_instance.save()
            return Response(
                {
                    "message": "투표 성공"
                },
                status=status.HTTP_200_OK
            )

#
