# Generated by Django 5.0.6 on 2024-06-10 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_instagramprofile_instagrampost_useranalysishistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranalysishistory',
            name='instagram_profile',
        ),
        migrations.RemoveField(
            model_name='useranalysishistory',
            name='user',
        ),
        migrations.DeleteModel(
            name='InstagramPost',
        ),
        migrations.DeleteModel(
            name='InstagramProfile',
        ),
        migrations.DeleteModel(
            name='UserAnalysisHistory',
        ),
    ]