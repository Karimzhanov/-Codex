# Generated by Django 5.0.6 on 2024-05-23 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_user_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='username пользователя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email адрес')),
                ('phone', models.CharField(max_length=255, verbose_name='Телефонный номер')),
                ('password', models.CharField(max_length=128, verbose_name='Пароль')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]