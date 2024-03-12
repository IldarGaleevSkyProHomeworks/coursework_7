from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny

from app_social_auth.utils import check_telegram_data
from app_telegrambot.models import TelegramUser


@api_view(['GET'])
@permission_classes([AllowAny])
def telegram_login(request):
    try:
        data = check_telegram_data(request.GET)
        user: TelegramUser = TelegramUser.objects.filter(telegram_user_id=int(data['id'])).first()
        if user:
            login(request, user.user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        raise NotFound('User not found')
    except (TimeoutError, ValueError, NotFound) as e:
        return redirect(reverse_lazy('login'))
        # return Response({'success': False, 'error': str(e)}, status.HTTP_401_UNAUTHORIZED)
