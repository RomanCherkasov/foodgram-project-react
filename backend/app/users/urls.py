from django.urls import include, path
from rest_framework import routers

from users.views import RegistrationAPIView

router = routers.DefaultRouter()

app_name = 'users'
