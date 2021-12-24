from os import access
from django.shortcuts import get_object_or_404
from api.models import User
from rest_framework.permissions import BasePermission
import jwt
from vote.settings.base import SECRET_KEY


def get_user(pk):
    return get_object_or_404(User, pk=pk)


'''
class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        access_token = request.COOKIES.get('access', None)
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
        user = get_user(payload.get('user_id'))
        return user.is_superuser


class IsOwnerOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        try:
            access_token = request.COOKIES.get('access', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            user = get_user(payload.get('user_id'))

            print(obj)
            print(user)

            return user.is_superuser or (obj == user)

        except(jwt.exceptions.DecodeError):
            return False 
        except(jwt.exceptions.InvalidAlgorithmError):
            return False
'''


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_superuser


class IsOwnerOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj == request.user or request.user.is_superuser)
