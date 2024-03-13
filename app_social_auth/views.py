import logging

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from app_social_auth.utils import check_telegram_data
from app_telegrambot import tasks
from app_telegrambot.models import TelegramUser

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def telegram_login(request):
    try:
        data = check_telegram_data(request.GET)
        user: TelegramUser = TelegramUser.objects.filter(telegram_user_id=int(data['id'])).first()
        if user:
            login(request, user.user)
            tasks.send_telegram_message.delay(
                user_id=user.user.id,
                md_text='Вы вошли в аккаунт'
            )

        password = User.objects.make_random_password()
        new_user: User = User.objects.create_user(
            username=data['username'] if data.get('username') else f'user_{data["id"]}',
            password=password
        )

        new_user.first_name = data.get('first_name')
        new_user.last_name = data.get('last_name')
        new_user.save()

        TelegramUser.objects.create(
            user=new_user,
            telegram_user_id=int(data['id'])
        )

        tasks.send_telegram_message.delay(
            user_id=new_user.id,
            md_text=f"Вы зарегистрировались на сайте "
                    f"[{settings.APPLICATION_HOSTNAME}]"
                    f"({settings.APPLICATION_SCHEME}://{settings.APPLICATION_HOSTNAME})\n"
                    f"Для входа используйте:\n"
                    f"Логин: `{new_user.username}`\n"
                    f"Пароль: ||{password}||"
        )

        return redirect(settings.LOGIN_REDIRECT_URL)
    except (TimeoutError, ValueError) as e:
        return redirect(reverse_lazy('login'))
        # return Response({'success': False, 'error': str(e)}, status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger.exception(f'Telegram login error {e}')