from datetime import datetime, timezone, timedelta

from celery import shared_task
from django.conf import settings

from app_habits.models import HabitNotification
from app_telegrambot import services


def get_now():
    return datetime.now(timezone.utc)


@shared_task
def send_habit_notifications():
    notifications = (
        HabitNotification.objects
        .filter(
            is_active=True,
            owner__is_active=True,
            owner__telegram_user__isnull=False,
        )
    )

    now_utc = get_now()

    for notification in notifications:

        uid = notification.owner.telegram_user.telegram_user_id
        target = notification.description

        timezone_time = now_utc.astimezone(notification.timezone)
        time_range_end = timezone_time + timedelta(seconds=settings.NOTIFICATION_SEND_TASK_INTERVAL)

        habits = notification.habits.filter(time__gte=timezone_time, time__lt=time_range_end)

        for habit in habits:
            services.send_text_message(
                telegram_uid=uid,
                md_text=f'{target} - {habit.action_description}'
            )
