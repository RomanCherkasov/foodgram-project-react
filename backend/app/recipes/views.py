from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from users.models import Favorite, Cart
from users.serializers import FavoriteRecipeSerializer
from recipes.models import Ingredients, Recipe, Tag
from recipes.serializers import (IngidientsSerializer, RecipesSerializer,
                                 TagSerializer)
from users.permissions import RegistredUser
from rest_framework.permissions import IsAuthenticated
from app.filters import IngredientsFilter
from app.paginator import Paginator


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngidientsSerializer
    permission_classes = [RegistredUser]
    filter_backends = (IngredientsFilter,)
    search_fields = ('^name',)
    lookup_url_kwarg = 'id'

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [RegistredUser]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [RegistredUser]
    pagination_class = Paginator
    # TODO CREATE FILTRES
    def perform_create(self, serializer):
        print(self.request.data.get('tags')[0])
        serializer.save(
            author=self.request.user,
        )

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite_add(self, request, id): #TODO maybe create method for add and delete
        if request.method == 'GET':
            if Favorite.objects.filter(
                user=request.user, recipe__id=id).exists():
                return Response({'error':'Recipe in favorite already'},
                status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=id)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            recipe = Favorite.objects.filter(user=request.user, recipe__id=id)
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error':'Recipe deleted already'},
            status=status.HTTP_400_BAD_REQUEST)
        return None

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def cart_add(self, request, id): #TODO maybe create method for add and delete
        if request.method == 'GET':
            if Cart.objects.filter(
                user=request.user, recipe__id=id).exists():
                return Response({'error':'Recipe in cart already'},
                status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=id)
            Cart.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            recipe = Cart.objects.filter(user=request.user, recipe__id=id)
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error':'Recipe deleted already'},
            status=status.HTTP_400_BAD_REQUEST)
        return None


