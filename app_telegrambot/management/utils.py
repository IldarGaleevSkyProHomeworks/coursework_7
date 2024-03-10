import logging

from django.conf import settings


def enable_console_log():
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