import logging

import telebot
from django.conf import settings
from django.urls import reverse_lazy

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Hello")


def process_webhook(updates_json: dict):
    update = telebot.types.Update.de_json(updates_json)
    bot.process_new_updates([update])


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
