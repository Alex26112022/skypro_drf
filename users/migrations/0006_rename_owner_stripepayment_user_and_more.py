# Generated by Django 5.0.7 on 2024-08-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_stripepayment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stripepayment',
            old_name='owner',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='stripepayment',
            name='course',
        ),
        migrations.AddField(
            model_name='stripepayment',
            name='course_id',
            field=models.PositiveIntegerField(default=0, verbose_name='Id курса'),
            preserve_default=False,
        ),
    ]
