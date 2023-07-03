from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from .serializers import CreateUserSerializer, LoginSerializer
from main.models import MyUser


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance_is_created = self.perform_create(serializer)
        if instance_is_created:
            user = authenticate(email=serializer.validated_data.get(
                'email'), password=serializer.validated_data.get('password1'))
            login(request, user)
            return redirect('main:homepage')
        return Response(status=401, data=serializer.errors)

    def perform_create(self, serializer):
        extra_fields = {
            'first_name': serializer.validated_data.get('first_name'),
            'last_name': serializer.validated_data.get('last_name'),
            'gender': serializer.validated_data.get('gender'),
            'photo': serializer.validated_data.get('photo')
        }
        user = MyUser.objects.create_user(
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password1'),
            **extra_fields
        )
        if user:
            return True
        return False

class LoginAPIView(APIView):

    def post(self, request: Request, *args, **kwargs) -> Response:

        if request.user.is_authenticated:
            return redirect('main:homepage')
        
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email = serializer.validated_data.get('email'), password = serializer.validated_data.get('password'))
        if user:
            login(request, user)
            return redirect('main:homepage')
        return Response(status=401, data={'error': 'Bad credentials'})
