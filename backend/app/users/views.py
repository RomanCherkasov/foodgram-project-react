from users.serializers import RegistrationSerializer, UserSerializer
from users.permissions import AdminOnly
from users.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

# class RegistrationAPIView(APIView):
#     perssions_classes = (AllowAny)
#     serializer_class = RegistrationSerializer

#     def post(self, request):
#         user = request.data
#         if request.data.get(
#             'username'
#         ) and request.data.get('username') == 'me':
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         data = {
#             'email': serializer.data.get('email'),
#             'id': serializer.data.get('id'),
#             'username': serializer.data.get('username'),
#             'first_name': serializer.data.get('first_name'),
#             'last_name': serializer.data.get('last_name'),
#         }

#         return Response(data, status=status.HTTP_200_OK)