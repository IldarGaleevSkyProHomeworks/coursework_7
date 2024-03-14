import logging

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from app_social_auth.utils import check_telegram_data
from app_telegrambot import tasks, message_text
from app_telegrambot.models import TelegramUser

logger = logging.getLogger(__name__)


@swagger_auto_schema(method='get', auto_schema=None)
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
                md_text=message_text.message_login()
            )
            return redirect(settings.LOGIN_REDIRECT_URL)

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

        login(request, new_user)

        tasks.send_telegram_message.delay(
            user_id=new_user.id,
            md_text=message_text.stack(
                message_text.message_welcome(),
                message_text.message_user_credentials(username=new_user.username, password=password)
            )
        )

        return redirect(settings.LOGIN_REDIRECT_URL)
    except (TimeoutError, ValueError) as e:
        return redirect(reverse_lazy('login'))
        # return Response({'success': False, 'error': str(e)}, status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger.exception(f'Telegram login error {e}')
