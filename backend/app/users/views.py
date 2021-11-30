from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
HTTP_201_CREATED, HTTP_204_NO_CONTENT)
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from users.serializers import SubscribeSerializer
from users.models import IsSubscribed
from app.paginator import Paginator

User = get_user_model()

class UserViewSet(UserViewSet):
    pagination_class = Paginator

    @action(detail=False, permission_classes=[IsAuthenticated])
    def allsubs(self, request):
        user = request.user
        queryset = IsSubscribed.objects.filter(user=user)
        page = self.paginate_queryset(queryset=queryset)
        serializer = SubscribeSerializer(
            page,
            many=True,
            context={'request': request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def sub(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({},status=HTTP_400_BAD_REQUEST)

        if IsSubscribed.objects.filter(user=user, author=author).exists():
            return Response({},status=HTTP_400_BAD_REQUEST)

        subscribe = IsSubscribed.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(
            subscribe, context={
                'request': request
            }
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    # https://stackoverflow.com/questions/62084905/how-to-make-delete-method-in-django-extra-action
    @sub.mapping.delete
    def unsub(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        subscribe = IsSubscribed.objects.create(user=user, author=author)
        if subscribe.exsist():
            subscribe.delete()
            return Response({}, status=HTTP_204_NO_CONTENT)

        return Response({}, status=HTTP_400_BAD_REQUEST)