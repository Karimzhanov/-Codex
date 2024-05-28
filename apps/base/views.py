from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from .models import Post, Comment, UserProfile
from django.utils import timezone
from django.contrib.auth.models import User
import instaloader, requests
from django.views.decorators.csrf import csrf_protect


# Create your views here.


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not (username and password and email and phone):
            error_message = 'Пожалуйста, заполните все поля.'
            return render(request, 'register.html', {'error_message': error_message})

        if password != confirm_password:
            error_message = 'Пароли не совпадают.'
            return render(request, 'register.html', {'error_message': error_message})

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            error_message = 'Пользователь с таким именем или электронной почтой уже существует.'
            return render(request, 'register.html', {'error_message': error_message})

        try:
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
            return render(request, 'register.html', {'error_message': error_message})

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

def analyze_instagram(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        post_count = int(request.POST.get('post_count', 10))  # По умолчанию отображаем 10 постов
        L = instaloader.Instaloader()

        try:
            # Аутентификация
            L.load_session_from_file('adm1n.06514')
            if not L.context.is_logged_in:
                L.login('adm1n.06514', 'admin_0677')  # Замените 'ваш_логин' и 'ваш_пароль' на ваши данные
                L.save_session_to_file()

            # Получаем профиль
            profile = instaloader.Profile.from_username(L.context, username)
            user_data = {
                'username': profile.username,
                'full_name': profile.full_name,
                'followers': profile.followers,
                'following': profile.followees, 
                'biography': profile.biography,
                'profile_pic_url': profile.profile_pic_url,
            }

            # Получаем посты из Instagram
            posts = []
            for i, post in enumerate(profile.get_posts()):
                if i >= post_count:
                    break
                new_post = {
                    'image_url': post.url,
                    'video_url': post.video_url, 
                    'caption': post.caption,
                    'likes': post.likes,
                    'comments': post.comments,
                    'timestamp': post.date_utc,
                }
                posts.append(new_post)
            return render(request, 'instagram_analysis.html', {'user_data': user_data, 'posts': posts})
        except Exception as e:
            error_message = f"Error: {str(e)}"
            return render(request, 'instagram_analysis.html', {'error_message': error_message})
    else:
        return render(request, 'instagram_analysis.html')




def post_list(request):
    posts = Post.objects.all()
    return render(request, 'instagram_analysis_result.html', {'posts': posts})

def sort_post_list(request):
    if request.method == 'GET':
        sort_by = request.GET.get('sort_by')
        if sort_by == 'date_asc':
            posts = Post.objects.order_by('pub_date')
        elif sort_by == 'date_desc':
            posts = Post.objects.order_by('-pub_date')
        elif sort_by == 'likes_asc':
            posts = Post.objects.order_by('likes')
        elif sort_by == 'likes_desc':
            posts = Post.objects.order_by('-likes')
        else:
            posts = Post.objects.all()
    return render(request, 'instagram_analysis_result.html', {'posts': posts})

def logout_view(request):
    logout(request)
    return redirect('register')


from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse


import requests
from django.http import HttpResponse

def proxy_view(request, url):
    # Используем переданный URL для отправки запроса на сервер Instagram
    response = requests.get(url)
    
    # Извлекаем тип контента из ответа
    content_type = response.headers.get('content-type', '')
    
    # Создаем HTTP-ответ с содержимым и типом контента из запроса к Instagram
    http_response = HttpResponse(response.content, content_type=content_type)
    
    # Добавляем заголовок Cross-Origin-Resource-Policy в зависимости от условий
    if 'instagram.ffru1-4.fna.fbcdn.net' in request.META.get('HTTP_ORIGIN', ''):
        http_response['Cross-Origin-Resource-Policy'] = 'same-site'
    else:
        http_response['Cross-Origin-Resource-Policy'] = 'cross-origin'
    
    return http_response


def settings(request):
    return render(request, 'settings.html')
