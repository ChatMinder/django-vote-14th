from django.shortcuts import get_object_or_404, render
from api.permissions import IsSuperuser

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.serializers import TokenSerializer, UserSerializer
from api.models import User

def get_user(self, pk):
    return get_object_or_404(User, pk=pk)


class UserView(APIView):
    permission_classes = [IsSuperuser,]

    def get(self, request):
        data = User.objects.all()
        serializer = UserSerializer(data=data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        user = get_user(pk)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class AuthView(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        pass

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass