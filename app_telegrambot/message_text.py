from datetime import timedelta

from django.conf import settings
from telebot.formatting import escape_markdown

from app_habits.models import Habit
from app_telegrambot.models import TelegramUser


def stack(*args):
    return '\n'.join(args)


def message_welcome() -> str:
    url = escape_markdown(f'{settings.APPLICATION_SCHEME}://{settings.APPLICATION_HOSTNAME}')
    return (f"Вы зарегистрировались на сайте "
            f"[{escape_markdown(settings.APPLICATION_HOSTNAME)}]"
            f"({escape_markdown(url)})")


def message_user_credentials(username, password) -> str:
    return (f"Для входа используйте:\n"
            f">Логин: `{escape_markdown(username)}`\n"
            f">Пароль: ||{escape_markdown(password)}||")


def message_login() -> str:
    return 'Вы вошли в аккаунт'


def message_jw_token_info(access, refresh) -> str:
    return ('Ваш токен:\n'
            '```json\n'
            '{\n'
            f'"refresh":"{refresh}",\n'
            f'"access":"{access}"\n'
            '}\n```')


def message_notifications_on_off(habit: Habit, is_enabled) -> str:
    return (f'{"📗" if is_enabled else "📕"} Вы {"включили" if is_enabled else "отключили"} '
            f'уведомления для\n'
            f'*\"{escape_markdown(habit.action_description)}\"*')


def message_notifications(habit: Habit) -> str:
    reward = habit.linked_habit.action_description if habit.linked_habit else habit.reward
    if reward:
        reward = f'Награда: *{escape_markdown(reward)}*\n'

    return (f'*{escape_markdown(habit.action_description)}*\n'
            f'{reward}'
            f'Продолжительность: *{timedelta(seconds=habit.duration)}*\n'
            f'Место: *{escape_markdown(habit.site)}*')


def message_start_new_user() -> str:
    return ('Давай знакомиться\\! Для этого вызови одну из комманд\\:\n\n'
            '\\- \\/link \\- чтобы привязать существующий аккаунт\n'
            '\\- \\/create \\- чтобы создать новый аккаунт\n')


def message_start_existed_user(accounts: list[TelegramUser]) -> str:
    return (escape_markdown('Ой! А я вас знаю, вот ваши аккаунты:') + '\n' +
            '\n'.join([f'\\- `{escape_markdown(account.user.username)}`' for account in accounts]))


def message_user_created() -> str:
    return 'Пользователь успешно создан'


def message_warning_user_exists() -> str:
    return 'Пользователь с таким логином уже существует'


def prompt_create_command_username(use_default_cmd, default_username) -> str:
    return f'Логин \\(`{escape_markdown(default_username)}` \\- /{use_default_cmd} \\- чтобы использовать предложенный\\):' if default_username else 'Логин\\:'


def prompt_create_command_password(gen_cmd) -> str:
    return f'Введите пароль \\(/{gen_cmd} \\- чтобы сгенерировать\\):'
