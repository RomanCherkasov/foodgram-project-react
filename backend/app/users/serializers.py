from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import IsSubscribed
User = get_user_model()

class RegistrationSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        )


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        flag = IsSubscribed.objects.filter(
            user=user, author=obj.id
        ).exists()
        return flag

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )