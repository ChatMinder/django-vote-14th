from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend

from .models import User


class LoginBackend(ModelBackend):
    def authenticate(self, request, login_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(login_id=login_id)
            if user.check_password(password):
                return user
            return None

        except User.DoesNotExist:
            return None


class TokenSerializer(TokenObtainPairSerializer):
    id = serializers.UUIDField(required=False, read_only=True)
    login_id = serializers.CharField(max_length=30, write_only=True)
    password = serializers.CharField(max_length=30, write_only=True)

    email = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['login_id'] = user.login_id
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_active'] = user.is_active
        token['is_staff'] = user.is_staff
        return token

    def validate(self, data):
        login_id = data.get('login_id')
        password = data.get('password')
        user = authenticate(login_id=login_id, password=password)
        if user is None:
            raise serializers.ValidationError(detail=True)

        validated_data = super().validate(data)
        refresh = self.get_token(user)
        validated_data["refresh"] = str(refresh)
        validated_data["access"] = str(refresh.access_token)
        validated_data["email"] = user.email
        validated_data["login_id"] = user.login_id
        validated_data["id"] = user.id

        return validated_data


class UserSerializer(serializers.ModelSerializer):
    login_id = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        login_id = validated_data.get('login_id')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            login_id=login_id,
            email=email
        )
        user.set_password(password)
        user.save()
        return user
