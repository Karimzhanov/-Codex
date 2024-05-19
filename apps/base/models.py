from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    username = models.CharField(
        max_length=255, 
        verbose_name="username пользователя "
    )
    email = models.EmailField(
        verbose_name="Почта пользователя",
        unique=True
    )
    password = models.CharField(
        max_length=255,  
        verbose_name="Пароль пользователя"
    )  # В реальном проекте пароль должен храниться в зашифрованном виде

    def __str__(self):
        return self.username

    
# models.py




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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Добавьте здесь другие поля, если это необходимо
