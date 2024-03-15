from celery import shared_task

from app_telegrambot import services


@shared_task
def send_telegram_message(user_id=None, telegram_uid=None, md_text: str = None):
    services.send_text_message(
        user_id=user_id,
        telegram_uid=telegram_uid,
        md_text=md_text
    )


@shared_task
def process_telegram_webhook_task(data: dict):
    services.process_webhook(data)
