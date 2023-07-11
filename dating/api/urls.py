from django.urls import path
from .views import CreateUserAPIView, LoginAPIView, SympathieMatch, UserListAPIView


app_name = 'api'

urlpatterns = [
    path('list/', UserListAPIView.as_view(), name='user_list'),
    path('clients/create/', CreateUserAPIView.as_view(), name='create_user'),
    path('clients/login/', LoginAPIView.as_view(), name='login_user'),
    path('clients/<int:id>/match/',
         SympathieMatch.as_view(), name='sympathie_match'),
]
