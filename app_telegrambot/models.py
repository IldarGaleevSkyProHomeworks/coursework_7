from django.contrib.auth.models import User
from django.db import models


class TelegramUser(models.Model):
    user = models.OneToOneField(
        User,
        related_name='telegram_user',
        on_delete=models.CASCADE,
    )

    telegram_user_id = models.BigIntegerField(
        verbose_name='Telegram user id'
    )
