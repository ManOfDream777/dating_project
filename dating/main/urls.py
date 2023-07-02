from django.urls import path
from .views import Homepage

app_name = 'main'

urlpatterns = [
    path('homepage/', Homepage.as_view(), name='homepage')
]