from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from recipes.models import Ingredients, Recipe, Tag
from recipes.serializers import (IngidientsSerializer, RecipesSerializer,
                                 TagSerializer)
from users.permissions import RegistredUser
from app.filters import IngredientsFilter


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngidientsSerializer
    permission_classes = [RegistredUser]
    filter_backends = (IngredientsFilter,)
    search_fields = ('^name',)
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
    # lookup_url_kwarg = 'id'
    
    # def get_queryset(self):
    #     return self.queryset

    # def get_object(self):
    #     id = self.kwargs.get(self.lookup_url_kwarg)
    #     return get_object_or_404(Tag, id=id)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [RegistredUser]

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(Recipe, id=id)

    # def create(self, request):
    #     print(request.data.get('ingredients'))
    #     return Response(request.data)

    def perform_create(self, serializer):
        print(self.request.data.get('tags')[0])
        serializer.save(
            author=self.request.user,
        )
