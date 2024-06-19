from . import serializers
from rest_framework import status
from django.db import transaction
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny


User=get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    '''
    Takes: user credentials (email, password, confirm_password)
    Performs:
        - Validates the provided data.
        - Creates a new user and generates an authentication token.
    Returns:
        - authentication token if registration is successful.
    '''
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class=serializers.UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
            token = Token.objects.create(user=user)
        return Response(
            {'token':token.key}, 
            status=status.HTTP_201_CREATED)


class UserLoginSerializer(ObtainAuthToken):
    '''
    Takes: user credentials (email and password)
    Performs:
        - Validates the provided credentials.
        - Retrieves or creates an authentication token for the user.
    Returns:
        - authentication token if login is successful.
    '''
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key}, status=status.HTTP_200_OK)


class Logout(APIView):
    '''
    Takes:
        - HTTP POST request with valid authentication credentials.
    Performs:
        - Deletes the authentication token associated with requesting user.
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
