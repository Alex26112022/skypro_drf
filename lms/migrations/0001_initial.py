# Generated by Django 5.0.7 on 2024-08-06 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Укажите название', max_length=255, null=True, verbose_name='Название')),
                ('preview', models.ImageField(blank=True, help_text='Загрузите картинку', null=True, upload_to='lms/course/preview')),
                ('description', models.TextField(blank=True, help_text='Сделайте описание', null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Укажите название', max_length=255, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, help_text='Сделайте описание', null=True, verbose_name='Описание')),
                ('preview', models.ImageField(blank=True, help_text='Загрузите картинку', null=True, upload_to='lms/lesson/preview')),
                ('video', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на урок')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson', to='lms.course', verbose_name='Курс')),
            ],
        ),
    ]
