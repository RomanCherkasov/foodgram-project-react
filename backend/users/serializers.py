from django.contrib.auth import get_user_model
from django.db.models import fields
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import Subscribe
from recipes.models import Recipe

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


class SubSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    email = serializers.ReadOnlyField(source='author.email')

    # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscribe
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        is_sub = Subscribe.objects.filter(
            user=obj.user,
            author=obj.author
        ).exists()
        print(is_sub)
        return is_sub

    def get_recipes(self, obj):
        return 'test'

    def get_recipes_count(self, obj):
        count = Recipe.objects.filter(author=obj.author).count()
        return count