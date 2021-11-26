from django.db import models
from django.db.models import fields, query
from rest_framework import serializers
from rest_framework.fields import SlugField

from recipes.models import Ingredients, Recipe, Tag
from users.serializers import UserSerializer


class IngidientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = (
            'id',
            'name',
            'measurement_unit',
        )

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )

class RecipesSerializer(serializers.ModelSerializer):

    ingredients = IngidientsSerializer(read_only=True)
    image = serializers.CharField()
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )