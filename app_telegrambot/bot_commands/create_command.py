import telebot
from django.contrib.auth.models import User
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message, BotCommand

from app_accounts.utils import generate_password
from app_telegrambot import message_text
from app_telegrambot.models import TelegramUser


class CreateAccountState(StatesGroup):
    username = State()
    password = State()


def init_cmd(bot: telebot.TeleBot):
    cmd_name = 'create'
    use_def_username_cmd = 'usethis'
    gen_pwd_cmd = 'gen'

    @bot.message_handler(commands=[cmd_name])
    def account_create_command_start_handler(message: Message):
        uid = message.from_user.id
        tg_username = message.from_user.username
        cid = message.chat.id

        bot.set_state(
            user_id=uid,
            chat_id=cid,
            state=CreateAccountState.username
        )

        msg = bot.send_message(
            chat_id=uid,
            parse_mode='MarkdownV2',
            text=message_text.prompt_create_command_username(use_def_username_cmd, tg_username)
        )

        with bot.retrieve_data(user_id=uid, chat_id=cid) as storage:
            storage['msg_id'] = msg.id

    def username_set_handle(user_id, chat_id, user_msg_id, username):
        with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as storage:
            mid = storage['msg_id']
            storage['username'] = username

            bot.set_state(
                user_id=user_id,
                chat_id=chat_id,
                state=CreateAccountState.password
            )

            bot.delete_message(
                chat_id=chat_id,
                message_id=mid
            )
            bot.delete_message(
                chat_id=chat_id,
                message_id=user_msg_id
            )

            msg = bot.send_message(
                chat_id=chat_id,
                parse_mode='MarkdownV2',
                text=message_text.prompt_create_command_password(gen_pwd_cmd)
            )

            storage['msg_id'] = msg.id

    @bot.message_handler(commands=[use_def_username_cmd], state=CreateAccountState.username)
    def account_create_command_username_use_default_handler(message: Message):
        uid = message.from_user.id
        cid = message.chat.id
        user_msg_id = message.id

        username = message.from_user.username
        username_set_handle(
            user_id=uid,
            chat_id=cid,
            username=username,
            user_msg_id=user_msg_id,
        )

    @bot.message_handler(state=CreateAccountState.username)
    def account_create_command_username_handler(message: Message):
        uid = message.from_user.id
        cid = message.chat.id
        user_msg_id = message.id

        username = message.text
        username_set_handle(
            user_id=uid,
            chat_id=cid,
            username=username,
            user_msg_id=user_msg_id,
        )

    def create_new_account_handle(tg_user, chat_id, user_msg_id, password):
        uid = tg_user.id

        with bot.retrieve_data(user_id=uid, chat_id=chat_id) as storage:
            mid = storage['msg_id']
            username = storage['username']
            storage.clear()

            bot.delete_state(
                user_id=uid,
                chat_id=chat_id,
            )

            bot.delete_message(
                chat_id=chat_id,
                message_id=mid
            )
            bot.delete_message(
                chat_id=chat_id,
                message_id=user_msg_id
            )

            existed_user = User.objects.filter(username=username).first()

            if existed_user:
                bot.send_message(
                    chat_id=uid,
                    parse_mode='MarkdownV2',
                    text=message_text.message_warning_user_exists()
                )
            else:
                new_user: User = User.objects.create_user(
                    username=username,
                    password=password
                )

                new_user.first_name = tg_user.first_name
                new_user.last_name = tg_user.last_name
                new_user.save()

                TelegramUser.objects.create(
                    user=new_user,
                    telegram_user_id=int(uid)
                )

                bot.send_message(
                    chat_id=uid,
                    parse_mode='MarkdownV2',
                    text=message_text.stack(
                        message_text.message_user_created(),
                        message_text.message_user_credentials(
                            username=username,
                            password=password
                        )
                    )
                )

    @bot.message_handler(commands=[gen_pwd_cmd], state=CreateAccountState.password)
    def create_account_command_password_gen_handler(message: Message):
        cid = message.chat.id
        tg_user = message.from_user
        user_msg_id = message.id

        password = generate_password()
        create_new_account_handle(
            tg_user=tg_user,
            chat_id=cid,
            user_msg_id=user_msg_id,
            password=password,
        )

    @bot.message_handler(state=CreateAccountState.password)
    def create_account_command_password_handler(message: Message):
        cid = message.chat.id
        tg_user = message.from_user
        user_msg_id = message.id

        password = message.text
        create_new_account_handle(
            tg_user=tg_user,
            chat_id=cid,
            user_msg_id=user_msg_id,
            password=password,
        )

    return BotCommand(
        command=cmd_name,
        description='Создать аккаунт на сайте'
    )
