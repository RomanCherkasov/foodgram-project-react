from django.urls import include, path
from rest_framework import routers

from users.views import RegistrationAPIView

router = routers.DefaultRouter()

auth_url = [
    path('users/', RegistrationAPIView.as_view()),
]

app_name = 'users'
urlpatterns = [
    path('api/', include(auth_url))
]