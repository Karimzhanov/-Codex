from django.apps import AppConfig

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.base'
    verbose_name = "Профиль Ползвателя"
    verbose_name_plural = "Профиль Ползвателя"
