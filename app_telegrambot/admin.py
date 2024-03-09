from django.contrib import admin

from app_telegrambot.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserModelAdmin(admin.ModelAdmin):
    pass
