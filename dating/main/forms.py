from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import MyUser

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label= 'Email', max_length=255)

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('last_name', 'first_name', 'email', 'gender', 'password1', 'password2')

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = "__all__"


