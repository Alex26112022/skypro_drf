from django.db import models

from config.settings import AUTH_USER_MODEL

options = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название',
                             help_text='Укажите название', **options)
    price = models.PositiveIntegerField(verbose_name='Стоимость', default=0)
    preview = models.ImageField(upload_to='lms/course/preview',
                                help_text='Загрузите картинку', **options)
    description = models.TextField(verbose_name='Описание',
                                   help_text='Сделайте описание', **options)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              related_name='course',
                              verbose_name='Пользователь', **options)
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата крайнего обновления',
                                      **options)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название',
                             help_text='Укажите название', **options)
    description = models.TextField(verbose_name='Описание',
                                   help_text='Сделайте описание', **options)
    preview = models.ImageField(upload_to='lms/lesson/preview',
                                help_text='Загрузите картинку', **options)
    video = models.CharField(max_length=255, verbose_name='Ссылка на урок',
                             **options)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,
                               verbose_name='Курс', related_name='lesson',
                               **options)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              related_name='lesson',
                              verbose_name='Пользователь', **options)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class SubscriptionToCourse(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='subscription',
                              verbose_name='Пользователь', **options)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='subscription',
                               verbose_name='Курс', **options)

    def __str__(self):
        return f'{self.owner} - {self.course}'

    class Meta:
        verbose_name = 'Подписка на курс'
        verbose_name_plural = 'Подписки на курсы'
