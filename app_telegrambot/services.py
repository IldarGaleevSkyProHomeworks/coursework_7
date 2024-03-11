import logging

import telebot
from django.conf import settings
from django.urls import reverse_lazy
from telebot.custom_filters import StateFilter
from telebot.types import Message
from app_telegrambot.bot_commands import link_command, start_command

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
bot.add_custom_filter(StateFilter(bot))

link_command.init_cmd(bot)
start_command.init_cmd(bot)

if settings.DEBUG:
    @bot.message_handler(content_types=['text'])
    def echo_messages(message: Message):
        uid = message.from_user.id
        bot.send_message(
            uid,
            parse_mode='html',
            text=f'echo: {message.text}'
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


def process_webhook(updates_json: dict):
    update = telebot.types.Update.de_json(updates_json)
    bot.process_new_updates([update])
