from django.http import Http404
from django.shortcuts import get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsOwnerOrSuperuser
from polls.models import *

from polls.serializers import CandidateSerializer, VoteSerializer
from rest_framework.views import APIView
from api.models import User


def get_user(pk):
    return get_object_or_404(User, pk=pk)


class CandidateList(APIView):
    def get(self, request):
        candidates = Candidate.objects.all().order_by('-votes')
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateDetail(APIView):
    def get_candidate(self, pk):
        return get_object_or_404(Candidate, pk=pk)

    def get(self, request, pk):
        candidate = self.get_candidate(pk=pk)
        serializer = CandidateSerializer(candidate)
        return Response(serializer)

    def put(self, request, pk):
        candidate = self.get_candidate(pk)
        serializer = CandidateSerializer(candidate)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, tatus=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):  # 특정 Post 삭제
        candidate = self.get_candidate(pk)
        candidate.delete()
        return Response("삭제 완료", status=status.HTTP_200_OK)

class CastVote(APIView):
    permission_classes = [IsOwnerOrSuperuser, ]

    def post(self, request):
        user = request.user
        serializer = VoteSerializer(data=request.data)
        if user.is_anonymous:
            return Response("알 수 없는 유저 입니다.", status=status.HTTP_404_NOT_FOUND)
        else:
            if user.voted:
                return Response(
                    {
                        "message": "이미 투표하셨습니다"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if serializer.is_valid():
                    serializer.create(validated_data=request.data)
                    user.voted = True
                    user.save()
                    return Response(
                        {
                            "message": "투표 성공"
                        },
                        status=status.HTTP_200_OK
                    )
                return Response(status=status.HTTP_400_BAD_REQUEST)
