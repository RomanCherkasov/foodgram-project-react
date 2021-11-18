from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.response import Response

from users.permissions import RegistredUser
from recipes.models import Ingredients, Tag
from recipes.serializers import IngidientsSerializer, TagSerializer

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