import telebot
from telebot.types import Message, BotCommand

from app_telegrambot import message_text
from app_telegrambot.models import TelegramUser


def init_cmd(bot: telebot.TeleBot):
    @bot.message_handler(commands=['start'])
    def start_command_handler(message: Message):
        uid = message.from_user.id
        accounts = TelegramUser.objects.filter(telegram_user_id=uid)

        if accounts.exists():
            bot.send_message(
                chat_id=uid,
                parse_mode='MarkdownV2',
                text=message_text.message_start_existed_user(accounts)
            )
        else:
            bot.send_message(
                chat_id=uid,
                parse_mode='MarkdownV2',
                text=message_text.message_start_new_user()
            )

    return BotCommand(
        command='start',
        description='Начало работы с ботом'
    )
