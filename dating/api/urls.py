from django.urls import path
from .views import CreateUserAPIView, LoginAPIView


app_name = 'api'


urlpatterns = [
    path('clients/create/', CreateUserAPIView.as_view(), name='create_user'),
    path('clients/login/', LoginAPIView.as_view(), name='login_user'),
]
