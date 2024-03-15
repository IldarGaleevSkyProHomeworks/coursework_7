from celery import shared_task

from app_habits.models import Habit
from app_telegrambot import services, message_text


@shared_task(bind=True)
def send_habit_notification(self, habit_id, telegram_user_id):
    habit: Habit = Habit.objects.filter(pk=habit_id).first()

    if habit:
        services.send_text_message(
            telegram_uid=telegram_user_id,
            md_text=message_text.message_notifications(habit)
        )
