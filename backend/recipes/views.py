from api.filters import FilterForAuthorAndTag, FilterForIngredients
from api.paginator import Paginator
from api.permissions import IsAdmin, IsAuthor
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, IngredientsInRecipe, Recipe, Tag
from recipes.serializers import (CartAndFavoriteSerializer,
                                 IngredientSerializer, RecipeSerializer,
                                 TagSerializer)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import Cart, Favorite


class TagViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (FilterForIngredients,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthor,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = Paginator
    filter_backends = (DjangoFilterBackend,)
    filter_class = FilterForAuthorAndTag

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        instance = Favorite.objects.filter(user=request.user, recipe__id=pk)
        if request.method == 'GET' and not instance.exists():
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = CartAndFavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        list = IngredientsInRecipe.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        response = HttpResponse(list, content_type='text/plain')
        filename_string = 'attachment; filename="shopping_list.txt"'
        response['Content-Disposition'] = filename_string
        return response

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        instance = Cart.objects.filter(user=request.user, recipe__id=pk)
        if request.method == 'GET' and not instance.exists():
            recipe = get_object_or_404(Recipe, id=pk)
            Cart.objects.create(user=request.user, recipe=recipe)
            serializer = CartAndFavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
