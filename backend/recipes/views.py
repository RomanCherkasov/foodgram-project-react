from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.permissions import IsAdmin, IsAuthor
from users.models import Favorite, Cart
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from recipes.models import Tag, Ingredient, Recipe, IngredientsInRecipe
from recipes.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, CartAndFavoriteSerializer
from api.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import FilterForIngredients, FilterForAuthorAndTag
from django.http import HttpResponse
from django.db.models import Sum

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
        if request.method == 'GET' and not (instance.exists()):
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = CartAndFavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and (instance.exists()):
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        list = IngredientsInRecipe.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount')).order_by()
        response = HttpResponse(list, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response


    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        instance = Cart.objects.filter(user=request.user, recipe__id=pk)
        if request.method == 'GET' and not (instance.exists()):
            recipe = get_object_or_404(Recipe, id=pk)
            Cart.objects.create(user=request.user, recipe=recipe)
            serializer = CartAndFavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and (instance.exists()):
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

