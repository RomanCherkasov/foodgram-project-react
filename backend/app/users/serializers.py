from rest_framework import serializers

from users.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(
        max_length=10,
        default='user',
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'role',
            'first_name',
            'last_name',
            'id',
        )
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
        )