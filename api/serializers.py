from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(source='user.password', write_only=True)

    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, data):
        user = User(
            login_id=data.get('login_id'),
            email=data.get('email'),
        )
        user.set_password(data.get('password'))
        user.save()
        return user