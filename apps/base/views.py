from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm
from .models import Post, Comment, UserProfile
from django.utils import timezone
from django.contrib.auth.models import User
import instaloader, requests, re 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if password == password_confirm:
                # Создаем пользователя с хэшированным паролем
                new_user = User.objects.create_user(username=username, email=email, password=password)
                # Создаем профиль пользователя
                user_profile = UserProfile(user=new_user)
                user_profile.save()

                return redirect('index')
            else:
                form.add_error('password_confirm', 'Passwords do not match')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
    
# @login_required
def index(request):
    latest_posts = Post.objects.all()[:10]
    comments = Comment.objects.filter(pub_date__gte=timezone.now() - timezone.timedelta(days=30))
    return render(request, 'index.html', {'latest_posts': latest_posts, 'comments': comments})

def edit_profile(request):
    # Ваш код для редактирования профиля пользователя
    return render(request, 'edit_profile.html')

# @login_required
def login(request):
    error_message = None
    if request.method == 'POST':
# @login_required
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
    return render(request, 'login.html', {'error_message': error_message})

def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})
from django.shortcuts import render
import instaloader

def analyze_instagram(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        post_count = int(request.POST.get('post_count', 10))  # По умолчанию отображаем 10 постов
        L = instaloader.Instaloader()

        try:
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
                # Проверяем, является ли контент видео
                if post.is_video:
                    new_post['video_url'] = post.video_url
                posts.append(new_post)

            return render(request, 'index.html', {'user_data': user_data, 'posts': posts})
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
