from django.urls import include, path

from api.views import UserViewSet
from djoser import views
from rest_framework.routers import DefaultRouter

app_name = 'users'
router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path(
        'auth/token/logout/',
        views.TokenDestroyView.as_view(),
        name='logout'
    ),
]
