# Generated by Django 5.0.6 on 2024-05-24 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_userprofile_profile_pic_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_pic_url',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватар'),
        ),
    ]