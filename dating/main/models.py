from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import MyUserManager


class MyUser(AbstractUser, models.Model):
    gender_choices = (
        ('M', ("Мужчина")),
        ('F', ("Женщина"))
    )

    username = None
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    email = models.EmailField(verbose_name='Email', unique=True)
    gender = models.CharField(choices=gender_choices,
                              max_length=7, verbose_name='Пол')
    photo = models.ImageField(verbose_name='Аватарка',
                              upload_to='user_photos/')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'gender',]

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('first_name', 'last_name')

    def get_full_name(self) -> str:
        return f'{self.last_name} {self.first_name[0]}'
