from django.urls import path
from .views import reset_password, send_reset_password_email

urlpatterns = [
    path('reset-password/', reset_password, name='reset_password'),
    path('send-reset-password-email/', send_reset_password_email, name='send_reset_password_email'),
]
