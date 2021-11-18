from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from users.permissions import RegistredUser
from recipes.models import Ingredients, Tag, Recipe
from recipes.serializers import IngidientsSerializer, TagSerializer, RecipesSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngidientsSerializer
    permission_classes = [RegistredUser]
    lookup_url_kwarg = 'id'

    def get_object(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(Ingredients, id=id)

    def get_queryset(self):
        return self.queryset

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [RegistredUser]
    lookup_url_kwarg = 'id'
    
    def get_queryset(self):
        return self.queryset

    def get_object(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(Tag, id=id)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [RegistredUser]

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(Recipe, id=id)

    def perform_create(self, serializer):
        print(self.kwargs)
        serializer.save()

    def perform_update(self, serializer):
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)