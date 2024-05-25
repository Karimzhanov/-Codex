"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-za^a!z22k0ap_t_p_3m1)&+ktqs43s_j(ir!+(48=7=eoxbr@u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'corsheaders',
    

    'apps.base',
    'apps.contacts',
    'apps.secondary',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.base.middleware.CORSMiddleware',  # Добавьте это

]

# settings.py

CORS_ALLOW_ALL_ORIGINS = True



ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



JAZZMIN_SETTINGS = {
    "site_title": "Instagram account analysis",  # Заголовок админ-панели
    "site_header": "Instagram account analysis",  # Заголовок на экране входа
    "site_brand": "Instagram account analysis",  # Бренд в верхней части админ-панели
    "welcome_sign": "Добро пожаловать в Instagram account analysis",  # Приветственное сообщение
    "site_title": "Instagram account analysis",  # Заголовок админ-панели
    "site_header": "Instagram account analysis",  # Заголовок на экране входа
    "site_brand": "Instagram account analysis",  # Бренд в верхней части админ-панели
    "welcome_sign": "Добро пожаловать в Instagram account analysis",  # Приветственное сообщение
    "search_model": ["auth.User", "blog.Post"],  # Модели, доступные для поиска
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    "show_sidebar": True,
    "changeform_format": "horizontal_tabs",
    "header_classes": "navbar-dark bg-dark",  # Темный фон верхней части админ-панели
    "header_color": "#000000",  # Черный цвет верхней части админ-панели
    "dark_mode_theme": True,  # Включить темный режим
    "show_language_chooser": True,  # Включить выбор языка в админ-панели
    "custom_css": None,  # Путь к пользовательскому CSS-файлу (если нужен)
    "show_ui_builder": True,  # Показать UI Builder
    "menu": [
        {
            "app": "index",  # Имя вашего приложения Django
            "name": "Основные параметры",  # Имя модели
            "icon": "fa fa-cogs",  # Иконка для меню
            "models": [
                {
                    "name": "Первая модель",  # Имя вашей модели
                    "icon": "fa fa-cog",  # Иконка для модели
                    "model": "index.Settings",  # Имя модели в формате "app_label.model_name"
                },
                # Добавьте другие модели, если необходимо
            ],
        },
        # Добавьте другие приложения и модели, если необходимо
    ],

}


# settings.py
EMAIL_HOST = 'smtp.example.com'  # SMTP-сервер
EMAIL_PORT = 587  # Порт SMTP-сервера
EMAIL_HOST_USER = 'adm1n.0651@gmail.com'  # Ваш адрес электронной почты
EMAIL_HOST_PASSWORD = 'Admin_admin'  # Пароль от вашей почты
EMAIL_USE_TLS = True  # Использовать ли TLS (SSL) для безопасного соединения
