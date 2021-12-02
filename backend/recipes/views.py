from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.permissions import IsAdmin, IsAuthor
from users.models import Favorite, Cart
from recipes.models import Tag, Ingredient, Recipe
from recipes.serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from api.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend

class TagViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthor,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = Paginator
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def favorite(self, request, pk=None):
        instance = Favorite.objects.filter(user=request.user, recipe__id=pk)
        if request.method == 'GET' and not (instance.exists()):
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and (instance.exists()):
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def shopping_cart(self, request, pk=None):
        instance = Cart.objects.filter(user=request.user, recipe__id=pk)
        if request.method == 'GET' and not (instance.exists()):
            recipe = get_object_or_404(Recipe, id=pk)
            Cart.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and (instance.exists()):
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

