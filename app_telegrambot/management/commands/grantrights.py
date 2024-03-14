from django.contrib.auth.models import User
from django.core.management import BaseCommand

from app_telegrambot import services
from app_telegrambot.models import TelegramUser


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--superuser',
            action='store_true',
            default=False,
            help='Add superuser rights',
        )

        parser.add_argument(
            '-s',
            '--staff',
            action='store_true',
            default=False,
            help='Add staff rights',
        )

        parser.add_argument(
            '--username',
            default=None,
            type=str,
            help='Account username',
            nargs='?',
        )

        parser.add_argument(
            '--telegramid',
            default=None,
            type=int,
            help='Telegram user Id',
            nargs='?',
        )

    def handle(self, *args, **options):
        is_staff = options['staff']
        is_superuser = options['superuser']

        is_staff = is_superuser or is_staff

        username = options['username']
        user_id = options['telegramid']

        if not (username or user_id):
            print('The given Username or Telegram user id must be set')
            return

        if username:
            user: User = User.objects.filter(username__iexact=username).first()
        else:
            user = TelegramUser.objects.filter(telegram_user_id=int(user_id)).first()
            if user:
                user: User = user.user

        if not user:
            print('User not found')
            return

        is_changed = False

        if user.is_staff != is_staff:
            print(f'is staff changed: {user.is_staff} -> {is_staff}')
            user.is_staff = is_staff
            is_changed = True

        if user.is_superuser != is_superuser:
            print(f'is superuser changed: {user.is_superuser} -> {is_superuser}')
            user.is_superuser = is_superuser
            is_changed = True

        if not is_changed:
            print('No changes')
        else:
            user.save()
            services.send_text_message(
                user_id=user.id,
                md_text="Вам изменили права доступа:\n```\n"                        
                        f"Суперпользователь: {is_superuser}\n"
                        f"Персонал:          {is_staff}\n"
                        "```"
            )
