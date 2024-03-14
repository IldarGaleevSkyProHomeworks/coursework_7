from datetime import time, datetime, timezone
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import override_settings

from app_habits.models import Habit, HabitNotification
from app_habits.tasks import send_habit_notifications
from app_telegrambot.models import TelegramUser


class HabitNotificationTestCase(TestCase):

    def setUp(self):
        user_1 = User.objects.create_user(username='User1', password='123')

        telegram_user_1 = TelegramUser.objects.create(user=user_1, telegram_user_id=1)

        habit_1 = Habit.objects.create(owner=user_1, is_pleasantly=False, action_description='action 1',
                                       time=time(1, 00))
        habit_2 = Habit.objects.create(owner=user_1, is_pleasantly=True, action_description='action 2',
                                       time=time(6, 00))
        habit_3 = Habit.objects.create(owner=user_1, is_pleasantly=False, action_description='action 3',
                                       time=time(22, 00))

        HabitNotification.objects.create(
            owner=user_1,
            description='UTC',
            timezone='Antarctica/Troll'
        ).habits.add(habit_1)

        HabitNotification.objects.create(
            owner=user_1,
            description='UTC+5',
            timezone='Antarctica/Vostok'
        ).habits.add(habit_2)

        HabitNotification.objects.create(
            owner=user_1,
            description='UTC-3',
            timezone='Antarctica/Rothera'
        ).habits.add(habit_3)

    @staticmethod
    def fake_func():
        return datetime(year=2024, month=1, day=1, hour=1, minute=0, tzinfo=timezone.utc)

    @override_settings(NOTIFICATION_SEND_TASK_INTERVAL=60)
    @patch('app_telegrambot.services.send_text_message')
    @patch('app_habits.tasks.get_now', side_effect=fake_func)
    def test_sending_notify_to_three_different_timezones(self, get_now, send_text_message: MagicMock):
        send_habit_notifications()

        message_count = send_text_message.call_count

        self.assertEqual(message_count, 3)
