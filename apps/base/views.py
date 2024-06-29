from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from apps.analyze_instagram.models import Post, Comment

from django.utils import timezone
from django.contrib.auth.models import User
import requests, re, phonenumbers


# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Проверка на заполнение всех полей
        if not (username and password and email and phone):
            error_message = 'Пожалуйста, заполните все поля.'
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})

        # # Проверка reCAPTCHA
        if not recaptcha_response:
            error_message = 'Подтвердите, что вы не робот.'
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})

        # Проверка reCAPTCHA с использованием Google reCAPTCHA API
        captcha_data = {
            'secret': '6LdXePMpAAAAAEyLkZ7gMZYg-Je93HddiMbYIaLQ',
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
        result = response.json()
        if not result['success']:
            error_message = 'Подтвердите, что вы не робот.'
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})

        # Обновленное регулярное выражение для проверки пароля
        password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$')
        if not password_pattern.match(password):
            error_message = 'Пароль должен содержать минимум 8 символов и состоять как минимум из одной буквы и одной цифры.'
            if not any(char.isdigit() for char in password):
                error_message += ' Пароль не содержит цифр.'
            if not any(char.isalpha() for char in password):
                error_message += ' Пароль не содержит букв.'
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})

        # Валидация номера телефона с использованием библиотеки phonenumbers
        try:
            parsed_phone = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed_phone):
                error_message = 'Введите корректный номер телефона.'
                return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})
            
            # Форматирование номера телефона в международный формат
            phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.phonenumberutil.NumberParseException:
            error_message = 'Введите корректный номер телефона.'
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})

        # Проверка на совпадение паролей
        if password != confirm_password:
            error_message = 'Пароли не совпадают.'
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})

        # Проверка на существующего пользователя с таким именем или email
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            error_message = 'Пользователь с таким именем или электронной почтой уже существует.'
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})

        try:
            # Создание нового пользователя
            user = User.objects.create_user(username=username, email=email, password=password)

            # Сохранение номера телефона и хэшированного пароля в профиль пользователя
            profile = UserProfile.objects.create(user=user, phone=phone, passwords=make_password(password))

            # Аутентификация пользователя и выполнение входа
            user = authenticate(request=request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('index')
        except Exception as e:
            error_message = f'Произошла ошибка при создании пользователя: {str(e)}'
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'email': email, 'phone': phone})

    return render(request, 'register.html')
# @login_required
def index(request):
    latest_posts = Post.objects.all()[:10]
    comments = Comment.objects.filter(pub_date__gte=timezone.now() - timezone.timedelta(days=30))

    if request.method == "POST":
        query = request.POST.get("search_query")

        # Получаем профиль текущего пользователя
        user_profile = request.user.profile

        # Сохраняем поисковой запрос для текущего пользователя
        user_profile.searches.add(query)
        user_profile.save()

        # Здесь можно выполнить какую-то логику для обработки поискового запроса

    return render(request, 'index.html', {'latest_posts': latest_posts, 'comments': comments})

def edit_profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        user.save()
        profile.save()

        return redirect('profile')

    return render(request, 'edit_profile.html', {'user': user})

# @login_required
def user_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            error_message = "Неверное имя пользователя или пароль"
    return render(request, 'login.html', {'error_message': error_message})


def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('register')



def settings(request):
    return render(request, 'settings.html')



def page_not_found(request, exception):
    return render(request, '404.html', status=404)
