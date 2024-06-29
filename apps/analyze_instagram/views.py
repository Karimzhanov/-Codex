
import os
from dotenv import load_dotenv
import logging
import instaloader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import UserProfile, Post, Comment

load_dotenv()

# Получаем значения из переменных окружения
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

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
                L.load_session_from_file(INSTAGRAM_USERNAME)
                logger.info("Сессия загружена успешно.")
            except FileNotFoundError:
                L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
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



@csrf_exempt
def proxy_view(request, url):
    try:
        # Декодируем URL, так как он может приходить в закодированном виде из запроса
        image_url = requests.utils.unquote(url)
        response = requests.get(image_url)
        
        if response.status_code != 200:
            return HttpResponseServerError("Не удалось загрузить изображение")

        # Создаем HTTP-ответ с содержимым изображения
        proxy_response = HttpResponse(response.content, content_type=response.headers['Content-Type'])

        # Устанавливаем заголовок Cross-Origin-Resource-Policy в зависимости от проверки происхождения
        if is_same_origin(image_url):
            proxy_response['Cross-Origin-Resource-Policy'] = 'same-site'
        else:
            proxy_response['Cross-Origin-Resource-Policy'] = 'cross-origin'

        return proxy_response
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return HttpResponseServerError("Внутренняя ошибка")

def is_same_origin(url):
    # Пример проверки на совпадение источника
    return 'instagram.com' in url
