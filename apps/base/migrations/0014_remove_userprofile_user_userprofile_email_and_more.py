# Generated by Django 5.0.6 on 2024-05-22 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True, verbose_name='Почта пользователя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.CharField(default=1, max_length=255, verbose_name='Пароль пользователя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(default=1, max_length=255, verbose_name='username пользователя '),
            preserve_default=False,
        ),
    ]
