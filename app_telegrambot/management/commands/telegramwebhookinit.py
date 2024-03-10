import logging.config

from django.conf import settings
from django.core.management import BaseCommand

from app_telegrambot.management.utils import enable_console_log
from app_telegrambot.services import init_webhook


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--delete',
            action='store_true',
            default=False,
            help='Delete webhook',
        )

    def handle(self, *args, **options):
        enable_console_log()
        init_webhook(options['delete'])
