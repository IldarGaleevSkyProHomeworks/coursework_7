from django.urls import path

from app_telegrambot.apps import AppTelegrambotConfig
from app_telegrambot.views import telegram_webhook

app_name = AppTelegrambotConfig.name

urlpatterns = [
    path('webhook/', telegram_webhook, name='telegram-webhook')
]
