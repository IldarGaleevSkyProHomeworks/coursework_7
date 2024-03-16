import logging

import telebot
from django.conf import settings
from django.urls import reverse_lazy
from rest_framework.exceptions import NotFound
from telebot.custom_filters import StateFilter
from telebot.types import Message
from telebot.util import antiflood

from app_telegrambot.bot_commands import (
    link_command,
    start_command,
    cancel_command,
    getjwt_command,
    genpass_command,
    create_command,
)
from app_telegrambot.models import TelegramUser

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
bot.add_custom_filter(StateFilter(bot))

commands = [
    cancel_command.init_cmd(bot),
    link_command.init_cmd(bot),
    start_command.init_cmd(bot),
    getjwt_command.init_cmd(bot),
    genpass_command.init_cmd(bot),
    create_command.init_cmd(bot),
]

bot.set_my_commands(
    commands=commands
)

if settings.DEBUG:
    @bot.message_handler(content_types=['text'])
    def echo_messages(message: Message):
        uid = message.from_user.id
        bot.send_message(
            uid,
            parse_mode='html',
            text=f'echo: {message.text}'
        )


def send_text_message(user_id=None, telegram_uid=None, md_text=None):
    if telegram_uid is None:
        user: TelegramUser = TelegramUser.objects.filter(user_id=user_id).first()
        if user is None:
            raise NotFound('User not found')
        telegram_uid = user.telegram_user_id

    antiflood(
        bot.send_message,
        chat_id=telegram_uid,
        parse_mode='MarkdownV2',
        text=md_text
    )


def start_poll():
    bot.infinity_polling(
        logger_level=logging.INFO,
        long_polling_timeout=settings.TELEGRAM_POLL_INTERVAL,
    )


def init_webhook(delete=False):
    if not settings.TELEGRAM_BOT_TOKEN:
        logging.warning('Telegram bot token not configured. Bot disabled.')
        return
    if delete:
        bot.delete_webhook()
        logging.info('Webhook deleted')
        return

    if not settings.TELEGRAM_USE_POLL and settings.APPLICATION_HOSTNAME:
        bot.set_webhook(f'{settings.APPLICATION_SCHEME}://{settings.APPLICATION_HOSTNAME}'
                        f'{reverse_lazy("telegram-bot:telegram-webhook")}')
        logging.info('Telegram bot ready')
        return

    logging.warning('App in poll-mode!')


def process_webhook(updates_json: dict):
    update = telebot.types.Update.de_json(updates_json)
    bot.process_new_updates([update])
