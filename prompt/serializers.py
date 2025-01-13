from rest_framework import serializers
from .models import Prompt
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class PromptSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  

    class Meta:
        model = Prompt
        fields = ['id', 'created_at', 'title', 'prompt_text', 'main_image', 'user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  
        return super().create(validated_data)
