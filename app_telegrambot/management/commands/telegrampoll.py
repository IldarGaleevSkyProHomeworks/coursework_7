import logging

from django.conf import settings
from django.core.management import BaseCommand

from app_telegrambot.management.utils import enable_console_log
from app_telegrambot.services import start_poll


class Command(BaseCommand):
    def handle(self, *args, **options):
        enable_console_log()
        if not settings.DEBUG:
            logging.warning('Please use Poll-mode only for debugging')

        logging.info('Bot poll started.\n\nStop poll with CTRL-BREAK')
        start_poll()
