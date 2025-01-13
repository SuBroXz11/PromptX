from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        return data
    
    def create(self, validated_data):
        user=User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'].lower(), # FOR CASE INSENSITIVE USERNAME
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        return validated_data
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username does not exist")
        return data
    
    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            return {'message': 'Invalid credentials', 'data': {}}
        
        refresh = RefreshToken.for_user(user)
        return {
            'message': 'Login successful',
            'data': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }