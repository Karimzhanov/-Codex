# Generated by Django 5.0.6 on 2024-06-11 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_usersearch_delete_instagramsearch'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserSearch',
        ),
    ]
