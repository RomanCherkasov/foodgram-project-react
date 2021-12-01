from django.contrib.auth import get_user_model
from django.db.models import fields
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

"""
Тут мы создаем кастомные сериализаторы для создания и получения юзера
"""

User = get_user_model()

class RegistrationSerializer(UserCreateSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
        'username', 'email', 'password')

class GetUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
        'username', 'email',)