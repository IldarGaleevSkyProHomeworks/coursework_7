import telebot
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message, BotCommand

from app_telegrambot.models import TelegramUser


class LoginState(StatesGroup):
    login = State()
    password = State()


def init_cmd(bot: telebot.TeleBot):
    @bot.message_handler(commands=['link'])
    def login_command_start_handler(message: Message):
        uid = message.from_user.id
        cid = message.chat.id

        bot.set_state(
            user_id=uid,
            chat_id=cid,
            state=LoginState.login
        )

        msg = bot.send_message(uid, "Введите ваш логин:")
        with bot.retrieve_data(user_id=uid, chat_id=cid) as storage:
            storage['msg_id'] = msg.id

    @bot.message_handler(state=LoginState.login)
    def login_command_login_handler(message: Message):
        login = message.text
        uid = message.from_user.id
        cid = message.chat.id

        with bot.retrieve_data(user_id=uid, chat_id=cid) as storage:
            mid = storage['msg_id']
            storage['login'] = login

            bot.set_state(
                user_id=uid,
                chat_id=message.chat.id,
                state=LoginState.password
            )

            bot.delete_message(
                chat_id=cid,
                message_id=mid
            )
            bot.delete_message(
                chat_id=cid,
                message_id=message.id
            )

            msg = bot.send_message(message.from_user.id, "Введите пароль:")

            storage['msg_id'] = msg.id

    @bot.message_handler(state=LoginState.password)
    def login_command_password_handler(message: Message):
        password = message.text
        uid = message.from_user.id
        cid = message.chat.id

        with bot.retrieve_data(user_id=uid, chat_id=cid) as storage:
            login = storage['login']
            mid = storage['msg_id']
            storage.clear()

        bot.delete_message(
            chat_id=cid,
            message_id=mid
        )

        bot.delete_message(
            chat_id=cid,
            message_id=message.id
        )

        bot.delete_state(
            user_id=uid,
            chat_id=cid
        )

        user: User = User.objects.filter(username=login).first()

        if not (user and check_password(password, user.password)):
            bot.send_message(uid, f'Пользователь с такими логином и паролем не найдены')
            return

        try:
            tuser, is_created = TelegramUser.objects.get_or_create(user_id=user.id, telegram_user_id=uid)
        except IntegrityError:
            bot.send_message(uid, f'Аккаунт уже привязан к другому пользователю')
            return

        if not is_created:
            bot.send_message(uid, f'Аккаунт уже привязан')
            return

        if not user.first_name:
            user.first_name = message.from_user.first_name
            user.last_name = message.from_user.last_name
            user.save()

        bot.send_message(uid, f'Аккаунт успешно привязан')

    return BotCommand(
        command='link',
        description='Привязать текущий Telegram-аккаунт к аккаунту на сайте'
    )
