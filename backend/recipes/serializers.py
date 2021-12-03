from django.core import validators
from django.db.models import fields
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.custom_fields import Base64ImageField
from recipes.models import Ingredient, Recipe, IngredientsInRecipe, Tag
from users.models import Cart, Favorite
from users.serializers import GetUserSerializer

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientsInRecipe.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
# Test commit
class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    tags = TagSerializer(read_only=True, many=True)
    author = GetUserSerializer(read_only=True)
    ingredients = IngredientsInRecipeSerializer(
        source='recipe_ingredient',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shoping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shoping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('author', 'tags',)

    def create(self, validated_data):
        image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe_obj = Recipe.objects.create(image=image, **validated_data)
        self.ingredients_create(
            ingredients,
            recipe_obj
        )
        recipe_obj.tags.set(tags)
        return recipe_obj

    def update(self, recipe, validated_data):
        if 'ingredients' in self.initial_data:
            recipe.ingredients.clear()
            self.ingredients_create(recipe, validated_data.pop('ingredients'))
        if 'tags' in self.initial_data:
            recipe.tags.set(validated_data.pop('tags'))
        return super().update(recipe, validated_data)

    def ingredients_create(self, ingredients, recipe):
        # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#bulk-create
        IngredientsInRecipe.objects.bulk_create([
            IngredientsInRecipe(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
                ) for ingredient in ingredients
        ])

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request.user.is_anonymous:
            return Recipe.objects.filter(
                favorite__user=request.user,
                id=obj.id
            ).exists()
        return False


    def get_is_in_shoping_cart(self, obj):
        request = self.context.get('request')
        if not request.user.is_anonymous:
            return Recipe.objects.filter(
                cart__user=request.user,
                id=obj.id
            ).exists()
        return False
    

    def validate(self, attrs):
        cooking_time = self.initial_data.get('cooking_time')
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        ingredients_data_list = []

        if int(cooking_time) > 0:
            attrs['cooking_time'] = cooking_time
        else:
            raise serializers.ValidationError('Cooking time validate error')

        if len(ingredients) >= 1:
            for ingredient in ingredients:
                ingredient_obj = get_object_or_404(
                    Ingredient,
                    id=ingredient['id']
                )
                if not ingredient_obj in ingredients:
                    ingredients_data_list.append(ingredient_obj)
                else:
                    raise serializers.ValidationError('ingredients validator error')

                if int(ingredient['amount']) <= 0:
                    raise serializers.ValidationError('ingredients validator error')
            attrs['ingredients'] = ingredients

        if tags and len(tags) >= len(set(tags)):
            attrs['tags'] = tags
        else:
            raise serializers.ValidationError('Tag validate error')
        return attrs
