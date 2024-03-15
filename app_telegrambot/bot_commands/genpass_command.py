import telebot
from django.contrib.auth.models import User
from telebot.types import Message, BotCommand

from app_telegrambot import message_text
from app_telegrambot.models import TelegramUser


def init_cmd(bot: telebot.TeleBot):
    @bot.message_handler(commands=['genpass'])
    def genpass_command_handler(message: Message):
        uid = message.from_user.id
        cid = message.chat.id

        curr_user = TelegramUser.objects.get(telegram_user_id=uid).user
        new_password = User.objects.make_random_password()
        curr_user.set_password(new_password)
        curr_user.save()

        bot.send_message(
            chat_id=uid,
            parse_mode="MarkdownV2",
            text=message_text.message_user_credentials(curr_user.username, new_password)
        )

    return BotCommand(
        command='genpass',
        description='Сгенерировать новый пароль аккаунта'
    )
