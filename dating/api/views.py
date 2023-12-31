from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http.response import Http404
from django.db.models import F

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CreateUserSerializer, LoginSerializer, SympathieSerializer, MyUserListSerializer
from .filters import UserFilter
from main.models import MyUser, Sympathie
from .services.services import get_distance_between_points


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

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data.get(
            'email'), password=serializer.validated_data.get('password'))
        if user:
            login(request, user)
            return redirect('main:homepage')
        return Response(status=401, data={'error': 'Bad credentials'})


class SympathieMatch(CreateAPIView):
    serializer_class = SympathieSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Sympathie.objects.none()

    # def get(self, request, *args, **kwargs):
    #     id_exists = MyUser.objects.filter(id=kwargs.get('id'))
    #     if id_exists.exists():
    #         return super().get(request, *args, **kwargs)
    #     return Response(status=404, data={'error': 'Пользователь не найден'})

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        u2 = MyUser.objects.filter(id=kwargs.get('id')).first()
        if u2 and u2 != self.request.user:
            status = Sympathie.create_if_not_exists(
                u1=self.request.user, u2=u2)
            if status:
                return Response(status=201, data={'email': u2.email})
            return Response(status=201)
        return Response(status=400, data=serializer.errors)


class UserListAPIView(ListAPIView):
    serializer_class = MyUserListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = UserFilter

    def get_queryset(self):
        query_distance = self.request.query_params.get('distance', None)
        if query_distance:
            query_distance = float(query_distance)
            qs = MyUser.objects.exclude(id=self.request.user.id).values(
                'id', 'longitude', 'latitude')
            user_ids = []
            for user in qs:
                distance, id = get_distance_between_points((self.request.user.latitude, self.request.user.longitude), (user.get(
                    'latitude'), user.get('longitude'))), user.get('id')
                if distance <= query_distance:
                    user_ids.append(id)
            return MyUser.objects.filter(id__in=user_ids)
        return MyUser.objects.exclude(id=self.request.user.id)
