from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from main.models import MyUser, Sympathie


class CreateUserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(
        min_length=8, max_length=20, label='Пароль', style={'input_type': 'password'})
    password2 = serializers.CharField(
        min_length=8, max_length=20, label='Подтверждение пароля', style={'input_type': 'password'})

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email',
                  'gender', 'photo', 'password1', 'password2')

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise ValidationError(
                {'password': 'Пароли не совпадают.'}, code=400)

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(
        min_length=2, max_length=20, label='Пароль', style={'input_type': 'password'})

    class Meta:
        fields = ('email', 'password')


class SympathieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sympathie
        exclude = ('is_mutual', )


class MyUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'gender', 'photo',)
