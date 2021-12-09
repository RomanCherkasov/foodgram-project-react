from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from users.models import Subscribe

User = get_user_model()

class GetUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'username', 'email',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Subscribe.objects.filter(
                user=user,
                author=obj.id
            ).exists()
        return False
