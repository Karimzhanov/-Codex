from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login,  name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('analyze-instagram/', views.analyze_instagram, name='analyze_instagram'),
    path('logout/', views.logout_view, name='logout'),
    re_path(r'^proxy/(?P<url>.+)$', views.proxy_view, name='proxy_view'),

]
