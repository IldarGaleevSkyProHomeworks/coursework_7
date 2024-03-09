import logging.config

from django.conf import settings
from django.core.management import BaseCommand

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
        logging.config.dictConfig({
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                }
            },
            "root": {
                "handlers": [
                    "console"
                ],
                "level": "DEBUG" if settings.DEBUG else "INFO"
            }
        })

        init_webhook(options['delete'])
