from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('analyze-instagram/', views.analyze_instagram, name='analyze_instagram'),
    path('proxy/<path:url>/', views.proxy_view, name='proxy_view'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
