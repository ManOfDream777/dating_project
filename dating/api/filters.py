from django_filters import rest_framework as filters

from main.models import MyUser

class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'gender')