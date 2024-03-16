import telebot
from rest_framework_simplejwt.tokens import RefreshToken
from telebot.types import Message, BotCommand

from app_telegrambot import message_text
from app_telegrambot.models import TelegramUser


def init_cmd(bot: telebot.TeleBot):
    @bot.message_handler(commands=['getjwt'])
    def getjwt_command_handler(message: Message):
        uid = message.from_user.id

        curr_user = TelegramUser.objects.get(telegram_user_id=uid).user
        token = RefreshToken.for_user(curr_user)
        bot.send_message(
            chat_id=uid,
            parse_mode="MarkdownV2",
            text=message_text.message_jw_token_info(
                access=str(token.access_token),
                refresh=str(token)
            )
        )

    return BotCommand(
        command='getjwt',
        description='Получить JWT'
    )
