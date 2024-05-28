from django.urls import path
from .views import reset_password, send_reset_password_email
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
    path('reset-password/', reset_password, name='reset_password'),
    path('send-reset-password-email/', send_reset_password_email, name='send_reset_password_email'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('settings/', send_reset_password_email, name='settings'),  # если это основная страница настроек
]
