from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from users.models import Subscribe
from users.serializers import SubSerializer
from api.paginator import Paginator
User = get_user_model()

class UserViewSet(UserViewSet):
    pagination_class = Paginator
    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author or Subscribe.objects.filter(
            user=user, author=author
        ).exists():
            return Response({'error':'something wrong'},status=status.HTTP_400_BAD_REQUEST)
        serializer = SubSerializer(
            Subscribe.objects.create(
                user=user,
                author=author
            ),
            context={
                'request': request
            }
        )
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        
        serializer = SubSerializer(
            self.paginate_queryset(Subscribe.objects.filter(user=request.user)),
            many=True, 
            context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        sub = Subscribe.objects.filter(user=request.user, author=author)
        if sub.exists() and request.user != author:
            sub.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)