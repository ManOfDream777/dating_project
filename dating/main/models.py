from typing import Any

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .managers import MyUserManager
from dating.settings import EMAIL_HOST_USER as host


class MyUser(AbstractUser, models.Model):

    gender_choices = (
        ('M', ("Мужчина")),
        ('F', ("Женщина"))
    )

    DISTANCE_CHOICES = (
        ('1', '1км'),
        ('3', '3км'),
        ('5', '5км'),
        ('10', '10км'),
        ('100', '100км'),
        ('300', '300км'),
        ('300+', '300+км'),
    )

    username = None
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    email = models.EmailField(verbose_name='Email', unique=True)
    gender = models.CharField(choices=gender_choices,
                              max_length=7, verbose_name='Пол')
    photo = models.ImageField(verbose_name='Аватарка',
                              upload_to='user_photos/')
    latitude = models.FloatField(verbose_name='Широта', default=0)
    longitude = models.FloatField(verbose_name='Долгота', default=0)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'gender', 'photo']

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('first_name', 'last_name')

    def get_full_name(self) -> str:
        return f'{self.last_name} {self.first_name[0]}'


@receiver(post_save, sender=MyUser)
def add_watermark(sender, instance: MyUser, created, **kwargs):
    if created:
        photo = Image.open(instance.photo.path)

        drawing = ImageDraw.Draw(photo)

        black = (3, 8, 12)
        font = ImageFont.load_default()
        drawing.text((300, 300), 'watermark', fill=black, font=font)

        photo.save(instance.photo.path)


class Sympathie(models.Model):
    TEMPLATE_NAME = 'email/email_notifications.txt'

    user1 = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                              verbose_name='Инициатор симпатии', related_name='sender')
    user2 = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                              verbose_name='Получатель симпатии', related_name='receiver')
    is_mutual = models.BooleanField(
        verbose_name='Взаимная симпатия', default=False)

    class Meta:
        verbose_name = 'Симпатия'
        verbose_name_plural = 'Симпатии'
        unique_together = (('user1', 'user2'), ('user2', 'user1'))

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__setattr__('email_message_was_sent_to_users', False)

    def __str__(self) -> str:
        return f'Симпатия между {self.user1.get_full_name()} и {self.user2.get_full_name()}'

    @staticmethod
    def sympathie_exists(u1: MyUser, u2: MyUser) -> object | None:
        return Sympathie.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: MyUser, u2: MyUser) -> bool:
        res = Sympathie.sympathie_exists(u1, u2)
        if not res:
            Sympathie.objects.create(user1=u1, user2=u2)
            return False
        else:
            sympathie = Sympathie.objects.get(
                Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1))
            sympathie.is_mutual = True
            sympathie.save()
            return True

    def send_emails_to_users(self) -> None:
        html_msg = render_to_string(self.TEMPLATE_NAME, context={
                                    'body': f'Вы понравились {self.user1.first_name}! Почта участника: {self.user1.email}', 'site_name': 'new-tinder 3.0', 'site_domain': 'http://test.ru'})
        plain_message = strip_tags(html_msg)
        send_mail(
            subject='Симпатия',
            message=plain_message,
            from_email=host,
            recipient_list=[self.user2.email],
            html_message=html_msg
        )

        html_msg = render_to_string(self.TEMPLATE_NAME, context={
                                    'body': f'Вы понравились {self.user2.first_name}! Почта участника: {self.user2.email}', 'site_name': 'new-tinder 3.0', 'site_domain': 'http://test.ru'})
        plain_message = strip_tags(html_msg)
        send_mail(
            subject='Симпатия',
            message=plain_message,
            from_email=host,
            recipient_list=[self.user1.email],
            html_message=html_msg
        )
        self.__setattr__('email_message_was_sent_to_users', True)

    def save(self, *args, **kwargs) -> None:
        if self.is_mutual:
            if not self.__getattribute__('email_message_was_sent_to_users'):
                self.send_emails_to_users()
        return super().save(*args, **kwargs)
