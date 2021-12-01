from django.shortcuts import render
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(UserViewSet):
    pass
