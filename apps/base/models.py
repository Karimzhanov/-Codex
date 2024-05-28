from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    phone = models.CharField(max_length=255, verbose_name=_("Телефонный номер"))
    searches = models.TextField(blank=True, null=True, verbose_name=_("Поисковые запросы"))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Аватар"))
    passwords = models.CharField(max_length=255, verbose_name=_("Пароль"))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Профиль пользователя")
        verbose_name_plural = _("Профили пользователей")


class Post(models.Model):
    image = models.ImageField(upload_to='posts/')
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
