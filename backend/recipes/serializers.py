from api.custom_fields import Base64ImageField
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, IngredientsInRecipe, Recipe, Tag
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.guserializer import GetUserSerializer
from users.models import Cart, Favorite


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
    print(f'id: {id}, name: {name}, m_u: {measurement_unit}')
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

class RecipeSerializer(serializers.ModelSerializer):
    print('serializer work')
    image = Base64ImageField(max_length=None, use_url=True)
    tags = TagSerializer(read_only=True, many=True)
    author = GetUserSerializer(read_only=True)
    ingredients = IngredientsInRecipeSerializer(
        source='ingredient_in_recipe',
        many=True,
        read_only=True,
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
        print('create!!!')
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
            self.ingredients_create(validated_data.pop('ingredients'), recipe)
        if 'tags' in self.initial_data:
            recipe.tags.set(validated_data.pop('tags'))
        return super().update(recipe, validated_data)

    def ingredients_create(self, ingredients, recipe):
        print('ingredients create!!!')
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
        print(request.user.is_anonymous)
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
        print(ingredients)
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
                print(f'ingredient_obj: {ingredient_obj}')
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
        print(attrs)
        return attrs


class CartAndFavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')

class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')


    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
            'user',
            'recipe',
        )
    def validate(self, attrs):
        user = attrs['user']
        recipe = attrs['recipe']
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Already exist')
        return attrs

class CartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Cart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
            'user',
            'recipe',
        )
    
    def validate(self, attrs):
        user = attrs['user']
        recipe = attrs['recipe']
        if Cart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Already exist')
        return attrs