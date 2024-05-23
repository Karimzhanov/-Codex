from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    phone = models.CharField(
        max_length=255,
        verbose_name="Телефонный номер"
    )
    groups = models.ManyToManyField(
        Group,
        related_name='user_custom_set',  # Уникальное имя для обратной ссылки
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_custom_set',  # Уникальное имя для обратной ссылки
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.username 
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


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
