from django.urls import path

from app_social_auth.apps import AppSocialAuthConfig
from app_social_auth.views import telegram_login

app_name = AppSocialAuthConfig.name

urlpatterns = [
    path('telegram/', telegram_login, name='telegram-login')
]
