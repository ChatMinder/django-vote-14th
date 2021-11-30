import jwt
from django.shortcuts import get_object_or_404, redirect


from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsOwnerOrSuperuser
from polls.models import *

from polls.serializers import CandidateSerializer, VoteSerializer
from rest_framework.views import APIView
from api.models import User
from vote.settings.base import SECRET_KEY


def get_user(pk):
    return get_object_or_404(User, pk=pk)


class CandidateViewSet(ModelViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()


class CastVote(APIView):
    permission_classes = [IsOwnerOrSuperuser, ]

    def post(self, request):
        access = request.COOKIES.get('access')

        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_user(pk=pk)
        serializer = VoteSerializer(data=request.data)
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

