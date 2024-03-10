from celery import shared_task

from app_telegrambot import services




@shared_task
def process_telegram_webhook_task(data: dict):
    services.process_webhook(data)
