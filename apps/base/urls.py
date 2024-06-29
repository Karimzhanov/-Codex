from django.urls import path, re_path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.user_login,  name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout_view, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

