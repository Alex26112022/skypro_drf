from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from lms.models import Course, Lesson

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


class Payments(models.Model):
    payment_methods = (
        ('CASH', 'Наличные'),
        ('TRANSFER TO ACCOUNT', 'Перевод на счет')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='payments')
    date_of_payment = models.DateField(verbose_name='Дата оплаты', **options)
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL,
                                    verbose_name='Оплаченный курс',
                                    related_name='payments', **options)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL,
                                    verbose_name='Оплаченный урок',
                                    related_name='payments', **options)
    payment_amount = models.FloatField(verbose_name='Сумма оплаты', **options)
    payment_method = models.CharField(max_length=255, choices=payment_methods,
                                      verbose_name='Метод оплаты', **options)

    def __str__(self):
        return f'{self.user} - {self.payment_amount} руб.'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
