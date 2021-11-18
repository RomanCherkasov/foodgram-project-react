from django.conf.urls import include
from django.urls import path
from recipes.views import IngredientViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', IngredientViewSet, basename='ingredients_id')

urlpatterns = [
    path('ingredients/', include(router.urls))
]