import jwt
import json

from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from api.models import User
from api.serializers import TokenSerializer, UserSerializer
from api.permissions import IsOwnerOrSuperuser, IsSuperuser

from vote.settings.base import SECRET_KEY

JWT_authenticator = JWTAuthentication()


def get_user(pk):
    return get_object_or_404(User, pk=pk)


class UserView(APIView):
    permission_classes = [IsSuperuser,]

    # 전체 유저 조회
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 회원가입
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserDetailView(APIView):
    permission_classes = [IsOwnerOrSuperuser,]

    # 특정 유저 조회
    def get(self, request, pk):
        user = get_user(pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    # 특정 유저 데이터 수정
    def patch(self, request, pk):
        user = get_user(pk=pk)
        self.check_object_permissions(request, user)
        data = JSONParser().parse(request)
        serializer = UserSerializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 특정 유저 삭제
    def delete(self, request, pk):
        user = get_user(pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class AuthView(APIView):
    permission_classes = [permissions.AllowAny,]

    # 토큰 주인 정보 조회
    def get(self, request):
        try :
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_user(pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 토큰 만료시 토큰 갱신
        except(jwt.exceptions.ExpiredSignatureError):
            data = {'refresh':request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_user(pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res

            raise jwt.exceptions.InvalidTokenError
        
        except(jwt.exceptions.InvalidTokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # access, refresh 토큰 생성 (로그인)
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            res = Response(serializer.data, status=status.HTTP_200_OK)
            res.set_cookie('access', serializer.data.get('access'))
            res.set_cookie('refresh', serializer.data.get('refresh'))
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # access, refresh 토큰 제거 (로그아웃)
    def delete(self, request):
        res = Response(status=status.HTTP_200_OK)
        res.set_cookie('access', '')
        res.set_cookie('refresh', '')
        return res

# httponly cookie를 반환
class AuthViewHttpOnly(APIView):
    permission_classes = [permissions.AllowAny,]

    # 토큰 주인 정보 조회
    def get(self, request):
        try :
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_user(pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 토큰 만료시 토큰 갱신
        except(jwt.exceptions.ExpiredSignatureError):
            data = {'refresh':request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_user(pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access, httponly=True)
                res.set_cookie('refresh', refresh, httponly=True)
                return res

            raise jwt.exceptions.InvalidTokenError
        
        except(jwt.exceptions.InvalidTokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # access, refresh 토큰 생성 (로그인)
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            res = Response(serializer.data, status=status.HTTP_200_OK)
            res.set_cookie('access', serializer.data.get('access'), httponly=True)
            res.set_cookie('refresh', serializer.data.get('refresh'), httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # access, refresh 토큰 제거 (로그아웃)
    def delete(self, request):
        res = Response(status=status.HTTP_200_OK)
        res.set_cookie('access', '', httponly=True)
        res.set_cookie('refresh', '', httponly=True)
        return res