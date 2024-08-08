from django.db import models

options = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название',
                             help_text='Укажите название', **options)
    preview = models.ImageField(upload_to='lms/course/preview',
                                help_text='Загрузите картинку', **options)
    description = models.TextField(verbose_name='Описание',
                                   help_text='Сделайте описание', **options)

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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
