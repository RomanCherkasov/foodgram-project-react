from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import IsSubscribed, User
from users.permissions import AdminOnly
from users.serializers import RegistrationSerializer, UserSerializer