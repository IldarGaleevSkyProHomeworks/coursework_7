from celery import shared_task

from app_telegrambot import services


@shared_task
def send_telegram_message(user_id: int, md_text: str):
    services.send_text_message(user_id, md_text)


@shared_task
def process_telegram_webhook_task(data: dict):
    services.process_webhook(data)
