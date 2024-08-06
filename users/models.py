from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

options = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, db_index=True,
                              verbose_name='E-mail',
                              help_text='Укажите E-mail')
    phone = PhoneNumberField(region='RU', verbose_name='Телефон',
                             help_text='Укажите телефон', **options)
    country = models.CharField(max_length=255, verbose_name='Город',
                               help_text='Укажите страну', **options)
    avatar = models.ImageField(upload_to='users/avatar', verbose_name='Аватар',
                               help_text='Загрузите аватар',
                               **options)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
