from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from .models import PasswordResetCode  # Импортируем модель для хранения кода сброса пароля

from core import settings

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Ссылка для сброса пароля отправлена на вашу почту.')
            return render(request, 'reset_password.html', {'form': form})
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})


def send_reset_password_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Генерируем код для сброса пароля
            reset_code = User.objects.make_random_password(length=6)
            # Сохраняем код в базе данных
            PasswordResetCode.objects.create(email=email, code=reset_code)
            # Ссылка для сброса пароля
            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[reset_code]))
            # Отправляем письмо с инструкциями по сбросу пароля
            email_subject = 'Сброс пароля'
            email_body = render_to_string('reset_password_email.html', {
                'reset_link': reset_link,
                'reset_code': reset_code,  # Включаем код в письмо
            })
            send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email])
            return HttpResponse('Ссылка для сброса пароля отправлена на вашу почту.')
        else:
            return HttpResponse('Пользователь с указанным адресом электронной почты не найден.')
    return render(request, 'send_reset_password_email.html')
