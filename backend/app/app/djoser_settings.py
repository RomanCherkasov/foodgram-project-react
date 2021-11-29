DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS':{
        'user_create': 'users.serializers.RegistrationSerializer',
        'user': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
    }
}
