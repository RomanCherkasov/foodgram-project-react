from django.conf.urls import include
from django.urls import path
from recipes.views import IngredientViewSet, TagViewSet, RecipeViewSet
from rest_framework import routers, viewsets

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients_id')
router.register('tags', TagViewSet, basename='tags_id')
router.register('recipes', RecipeViewSet, basename='recipe_id')

urlpatterns = [
    path('', include(router.urls))
]