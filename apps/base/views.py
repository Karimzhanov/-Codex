from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from .models import Post, Comment, UserProfile
from django.utils import timezone
from django.contrib.auth.models import User
import instaloader, requests, re, phonenumbers
from django.views.decorators.csrf import csrf_protect


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


import logging
import instaloader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
import requests
from .models import UserProfile, Post, Comment
logger = logging.getLogger(__name__)

@login_required
def analyze_instagram(request):
    if request.method == 'POST':                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        username = request.POST.get('username')
        post_count = int(request.POST.get('post_count', 10))
        if not username:
            error_message = "Не указано имя пользователя."
            logger.error(error_message)
            return render(request, 'instagram_analysis.html', {
                'error_message': error_message,
                'username': username,
                'post_count': post_count
            })

        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if user_profile.searches:
            user_profile.searches += f",{username}"
        else:
            user_profile.searches = username
        user_profile.save()

        cache_key = f'instagram_profile_{username}_{post_count}'
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f'Данные получены из кэша для пользователя {username}')
            return render(request, 'instagram_analysis.html', cached_data)

        L = instaloader.Instaloader()

        try:
            try:
                L.load_session_from_file('karimzhanov_kgz')
                logger.info("Сессия загружена успешно.")
            except FileNotFoundError:
                L.login('karimzhanov_kgz', 'kukushaaa')
                L.save_session_to_file()
                logger.info("Сессия сохранена успешно.")

            if not L.context.is_logged_in:
                raise Exception("Ошибка аутентификации. Пожалуйста, проверьте логин и пароль.")

            profile = instaloader.Profile.from_username(L.context, username)
            user_data = {
                'username': profile.username,
                'full_name': profile.full_name,
                'followers': profile.followers,
                'following': profile.followees,
                'biography': profile.biography,
                'profile_pic_url': profile.profile_pic_url,
            }

            posts = []
            thirty_days_ago = datetime.now() - timedelta(days=30)
            for i, post in enumerate(profile.get_posts()):
                if i >= post_count:
                    break

                comments = []
                for comment in post.get_comments():
                    if comment.created_at_utc > thirty_days_ago:
                        comments.append({
                            'text': comment.text,
                            'created_at': comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S"),
                            'author': comment.owner.username
                        })

                images = []
                videos = []

                if post.typename == 'GraphImage':
                    images.append(post.url)
                elif post.typename == 'GraphVideo':
                    videos.append(post.video_url)
                elif post.typename == 'GraphSidecar':
                    for sidecar in post.get_sidecar_nodes():
                        if sidecar.is_video:
                            videos.append(sidecar.video_url)
                        else:
                            images.append(sidecar.display_url)

                new_post = {
                    'image_urls': images,
                    'video_urls': videos,
                    'caption': post.caption or '',
                    'likes': post.likes,
                    'comments': comments,
                    'timestamp': post.date_utc.strftime("%Y-%m-%d %H:%M:%S"),
                }
                posts.append(new_post)

                # Сохранение постов и комментариев в базу данных
                post_obj = Post.objects.create(
                    user_profile=user_profile,
                    description=post.caption or '',
                    likes=post.likes,
                    video_url=','.join(videos)
                )

                for image_url in images:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        post_obj.image.save(f"{post_obj.id}.jpg", ContentFile(response.content))

                for comment in comments:
                    Comment.objects.create(
                        post=post_obj,
                        text=comment['text'],
                        pub_date=comment['created_at'],
                        author=comment['author']
                    )

            # Загрузка историй (Stories)
            stories = []
            for story in L.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    story_images = []
                    story_videos = []
                    if item.is_video:
                        story_videos.append(item.video_url)
                    else:
                        story_images.append(item.url)

                    stories.append({
                        'image_urls': story_images,
                        'video_urls': story_videos,
                        'timestamp': item.date_utc.strftime("%Y-%m-%d %H:%M:%S"),
                    })

            context = {
                'user_data': user_data,
                'posts': posts,
                'stories': stories,
                'username': username,
                'post_count': post_count
            }

            cache.set(cache_key, context, timeout=60*60)
            logger.info(f'Данные закэшированы для пользователя {username}')

            return render(request, 'instagram_analysis.html', context)

        except instaloader.exceptions.ConnectionException as e:
            error_message = f"Ошибка соединения: {str(e)}"
            logger.error(error_message)
            return render(request, 'instagram_analysis.html', {
                'error_message': error_message,
                'username': username,
                'post_count': post_count
            })
        except instaloader.exceptions.BadCredentialsException as e:
            error_message = "Ошибка аутентификации. Пожалуйста, проверьте логин и пароль."
            logger.error(error_message)
            return render(request, 'instagram_analysis.html', {
                'error_message': error_message,
                'username': username,
                'post_count': post_count
            })
        except Exception as e:
            error_message = f"Произошла ошибка: {str(e)}"
            logger.error(error_message)
            return render(request, 'instagram_analysis.html', {
                'error_message': error_message,
                'username': username,
                'post_count': post_count
            })

    logger.info('Возвращение пустого шаблона для GET-запроса')
    return render(request, 'instagram_analysis.html', {'username': '', 'post_count': 10})





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
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proxy_view(request, url):
    try:
        image_url = requests.utils.unquote(url)
        
        response = requests.get(image_url)
        
        if response.status_code != 200:
            return HttpResponseServerError("Не удалось загрузить изображение")

        proxy_response = HttpResponse(response.content, content_type=response.headers['Content-Type'])

        if is_same_origin(image_url):
            proxy_response['Cross-Origin-Resource-Policy'] = 'same-site'
        else:
            proxy_response['Cross-Origin-Resource-Policy'] = 'cross-origin'

        return proxy_response

    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return HttpResponseServerError("Внутренняя ошибка сервера")

def is_same_origin(url):
    # Пример проверки на совпадение источника
    return 'example.com' in url


def settings(request):
    return render(request, 'settings.html')



def page_not_found(request, exception):
    return render(request, '404.html', status=404)
