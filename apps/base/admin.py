# admin.py
from django.contrib import admin
from .models import  UserProfile # Обновленный импорт

admin.site.register(UserProfile)
