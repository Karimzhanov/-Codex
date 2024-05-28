from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

def reset_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Пароль успешно изменен.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Произошла ошибка при изменении пароля.')
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'reset_password.html', {'form': form})

def send_reset_password_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                reset_code = default_token_generator.make_token(user)
                reset_link = request.build_absolute_uri(
                    reverse_lazy('password_reset_confirm', kwargs={'uidb64': user.pk, 'token': reset_code})
                )
                email_subject = 'Сброс пароля'
                email_body = f"""
                Здравствуйте,

                Вы получили это письмо, потому что запросили сброс пароля для вашей учетной записи.

                Для сброса пароля перейдите по следующей ссылке:
                {reset_link}

                Ваш код для сброса пароля: {reset_code}

                Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.

                С уважением,
                Ваша команда поддержки
                """

                try:
                    send_mail(
                        email_subject, 
                        '',  # Пустое тело для текстовой версии
                        settings.DEFAULT_FROM_EMAIL, 
                        [email],
                        fail_silently=False,
                        html_message=email_body  # Указываем, что сообщение является HTML
                    )
                    messages.success(request, 'Ссылка для сброса пароля отправлена на вашу почту.')
                except Exception as e:
                    logger.error(f'Ошибка при отправке email: {e}')
                    messages.error(request, 'Произошла ошибка при отправке письма.')
                
                return redirect('settings')
            else:
                messages.error(request, 'Пользователь с указанным адресом электронной почты не найден.')
        else:
            messages.error(request, 'Введите адрес электронной почты.')
    return render(request, 'settings.html')
