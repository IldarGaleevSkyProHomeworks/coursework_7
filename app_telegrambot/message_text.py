from django.conf import settings


def stack(*args):
    return '\n'.join(args)


def message_welcome() -> str:
    return (f"Вы зарегистрировались на сайте "
            f"[{settings.APPLICATION_HOSTNAME}]"
            f"({settings.APPLICATION_SCHEME}://{settings.APPLICATION_HOSTNAME})")


def message_user_credentials(username, password) -> str:
    return (f"Для входа используйте:\n"
            f">Логин: `{username}`\n"
            f">Пароль: ||{password}||")


def message_login() -> str:
    return 'Вы вошли в аккаунт'


def message_jw_token_info(access, refresh) -> str:
    return ('Ваш токен:\n'
            '```json\n'
            '{\n'
            f'"refresh":"{refresh}",\n'
            f'"access":"{access}"\n'
            '}\n```')
