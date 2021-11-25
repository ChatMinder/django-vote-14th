from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend

from .models import User

class LoginBackend(ModelBackend):
    def authenticate(self, request, login_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(login_id=login_id)
            if user.check_password(password):
                print("success")
                return user
            print("fail")
            return None

        except User.DoesNotExist:
            return None

class TokenSerializer(TokenObtainPairSerializer):
    id = serializers.UUIDField(required=False, read_only=True)
    login_id = serializers.CharField(max_length=30, write_only=True)
    password = serializers.CharField(max_length=30, write_only=True)
    token = serializers.CharField(read_only=True)


    def validate(self, data):
        login_id = data.get('login_id')
        password = data.get('password')
        user = authenticate(login_id=login_id, password=password)
        if user is None:
            raise serializers.ValidationError(detail=True)
        
        id = user.id
        token = super().get_token(user)
        
        return {
            'id':id,
            'login_id':login_id,
            'token':token
        }


class UserSerializer(serializers.ModelSerializer):
    login_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.CharField()

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