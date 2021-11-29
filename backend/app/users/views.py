from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
HTTP_201_CREATED)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from users.models import IsSubscribed

User = get_user_model()

class UserViewSet(UserViewSet):
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({},status=HTTP_400_BAD_REQUEST)

        if IsSubscribed.objects.filter(user=user, author=author).exists():
            return Response({},status=HTTP_400_BAD_REQUEST)

        subscribe = IsSubscribed.objects.create(user=user, author=author)
        #TODO SERIALIZER!!!