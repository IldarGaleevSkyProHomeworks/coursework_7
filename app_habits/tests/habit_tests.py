from datetime import time
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import status

from app_habits.models import Habit
from app_habits.views import HabitViewSet
from app_telegrambot import message_text
from app_telegrambot.models import TelegramUser


class HabitTestCase(TestCase):

    def setUp(self):
        self.general_user_owner = User.objects.create_user(username='GeneralUserOwner', password='123')
        self.general_user = User.objects.create_user(username='GeneralUser', password='123')
        self.super_user = User.objects.create_superuser(username='SuperUser', password='123')

        self.telegram_user = TelegramUser.objects.create(user=self.general_user_owner, telegram_user_id=1)

        self.public_non_pleasantly_habit = Habit.objects.create(
            owner=self.general_user_owner,
            is_pleasantly=False,
            action_description='action 1',
            time=time(1, 00),
            is_public=False,
            reward="Reward",
        )

        self.public_pleasantly_habit = Habit.objects.create(
            owner=self.general_user_owner,
            is_pleasantly=True,
            action_description='action 1',
            time=time(1, 00),
            is_public=False,
            reward="Reward",
        )

        self.non_public_habit = Habit.objects.create(
            owner=self.general_user_owner,
            is_pleasantly=False,
            action_description='action 1',
            time=time(1, 00),
            is_public=False,
            reward="Reward",
        )

        self.non_general_user_owner_habit_1 = Habit.objects.create(
            owner=self.general_user,
            is_pleasantly=True,
            action_description='action 1',
            time=time(1, 00),
            is_public=False,
            reward="Reward",
        )

        self.non_general_user_owner_habit_2 = Habit.objects.create(
            owner=self.super_user,
            is_pleasantly=False,
            action_description='action 1',
            time=time(1, 00),
            is_public=False,
            reward="Reward",
        )

        self.general_user_owner.save()
        self.general_user.save()
        self.super_user.save()
        self.public_non_pleasantly_habit.save()
        self.public_pleasantly_habit.save()
        self.non_public_habit.save()
        self.non_general_user_owner_habit_1.save()
        self.non_general_user_owner_habit_2.save()

    def check_create_habit(self, test_data, user):
        self.client.force_login(user)
        url = reverse('api:habits-list')
        response = self.client.post(url, data=test_data)
        return response.status_code, response.data

    def check_list_habit(self, user, count):
        self.client.force_login(user)
        url = reverse('api:habits-list')
        response = self.client.get(url)
        result_count = response.json()['count']

        self.assertEqual(result_count, count)

    def check_retrieve_habit(self, user, status_code):
        self.client.force_login(user)
        url = reverse('api:habits-detail', args=[self.non_public_habit.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def check_update_habit(self, user, status_code):
        self.client.force_login(user)
        url = reverse('api:habits-detail', args=[self.non_public_habit.pk])
        response = self.client.patch(
            url,
            data={"time": "22:00"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status_code)

    def check_delete_habit(self, user, status_code):
        self.client.force_login(user)
        url = reverse('api:habits-detail', args=[self.non_public_habit.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status_code)

    def test_list_habit_by_general_user_returns_3(self):
        self.check_list_habit(self.general_user_owner, 3)

    def test_list_habit_by_super_user_returns_5(self):
        self.check_list_habit(self.super_user, 5)

    def test_retrieve_habit_by_owner_success(self):
        self.check_retrieve_habit(self.general_user_owner, status.HTTP_200_OK)

    def test_retrieve_habit_by_non_owner_not_found(self):
        self.check_retrieve_habit(self.general_user, status.HTTP_404_NOT_FOUND)

    def test_retrieve_habit_by_super_user_success(self):
        self.check_retrieve_habit(self.super_user, status.HTTP_200_OK)

    def test_update_habit_by_owner_success(self):
        self.check_update_habit(self.general_user_owner, status.HTTP_200_OK)

    def test_update_habit_by_non_owner_not_found(self):
        self.check_update_habit(self.general_user, status.HTTP_404_NOT_FOUND)

    def test_update_habit_by_super_user_success(self):
        self.check_update_habit(self.super_user, status.HTTP_200_OK)

    def test_delete_habit_by_owner_success(self):
        self.check_delete_habit(self.general_user_owner, status.HTTP_204_NO_CONTENT)

    def test_delete_habit_by_non_owner_not_found(self):
        self.check_delete_habit(self.general_user, status.HTTP_404_NOT_FOUND)

    def test_delete_habit_by_super_user_success(self):
        self.check_delete_habit(self.super_user, status.HTTP_204_NO_CONTENT)

    def test_create_validation_success(self):
        data = {
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": True,
            "periodic": 1,
            "duration": 0,
            "is_public": True
        }

        status_code, _ = self.check_create_habit(data, self.general_user)

        self.assertEqual(status_code, status.HTTP_201_CREATED)

    def test_create_validation_linked_habit_not_own_or_public_failed(self):
        data = {
            "linked_habit": self.non_general_user_owner_habit_1.id,
            "time": "10:00",
            "site": "gnusnyy test",
            "action_description": "padla",
            "is_pleasantly": False,
            "periodic": 1,
            "duration": 0,
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['linked_habit'][0], 'Связанная привычка должна быть публичной или вашей')

    def test_create_validation_linked_habit_not_is_pleasantly_failed(self):
        data = {
            "linked_habit": self.public_non_pleasantly_habit.id,
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": False,
            "periodic": 1,
            "duration": 0,
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['linked_habit'][0], 'Связанная привычка должна быть приятной')

    def test_create_validation_pleasantly_habit_set_linked_habit_failed(self):
        data = {
            "linked_habit": self.public_pleasantly_habit.id,
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": True,
            "periodic": 1,
            "duration": 0,
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['linked_habit'][0], 'У приятной привычки не может быть связанной привычки')

    def test_create_validation_pleasantly_habit_set_duration_more_than_two_minutes_failed(self):
        data = {
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": True,
            "periodic": 1,
            "duration": 500,
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['duration'][0], 'Приятная привычка не должна длиться больше двух минут')

    def test_create_validation_pleasantly_habit_set_reward_failed(self):
        data = {
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": True,
            "periodic": 1,
            "duration": 0,
            "reward": "string",
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['reward'][0], 'У приятной привычки не может быть награды')

    def test_create_validation_non_pleasantly_habit_reward_and_linked_habit_not_set_failed(self):
        data = {
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": False,
            "periodic": 1,
            "duration": 0,
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['linked_habit'][0], 'Укажите награду или связанную привычку')
        self.assertEqual(result['reward'][0], 'Укажите награду или связанную привычку')

    def test_create_validation_non_pleasantly_habit_reward_and_linked_habit_is_set_failed(self):
        data = {
            "linked_habit": self.public_pleasantly_habit.id,
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": False,
            "periodic": 1,
            "duration": 0,
            "reward": "string",
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['linked_habit'][0], 'Если указана награда, связанную привычку указать нельзя')
        self.assertEqual(result['reward'][0], 'Если указана связанная привычка, награду указывать нельзя')

    def start_stop_notifications(self, send_telegram_message, is_start):
        habit = self.non_public_habit

        self.client.force_login(self.general_user_owner)

        if is_start:
            url = reverse('api:habits-start', args=[habit.pk])
            response = self.client.post(
                path=url,
                data={"timezone": "Antarctica/Troll"},
                content_type="application/json"
            )
        else:
            url = reverse('api:habits-stop', args=[habit.pk])
            response = self.client.delete(
                path=url,
            )

        send_telegram_message.assert_called_with(
            telegram_uid=self.telegram_user.telegram_user_id,
            md_text=message_text.message_notifications_on_off(habit, is_start)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('app_telegrambot.tasks.send_telegram_message.delay')
    def test_start_notification_success(self, send_telegram_message: MagicMock):
        self.start_stop_notifications(send_telegram_message, True)

    @patch('app_telegrambot.tasks.send_telegram_message.delay')
    def test_start_existed_notification_no_send_message(self, send_telegram_message: MagicMock):
        habit = self.non_public_habit

        self.client.force_login(self.general_user_owner)

        PeriodicTask.objects.create(
            name=HabitViewSet.get_task_name(
                habit_id=habit.id,
                tg_user_id=self.telegram_user.telegram_user_id,
            ),
            crontab=CrontabSchedule.objects.create(
                hour=habit.time.hour,
                minute=habit.time.minute,
                day_of_month=f'*/{habit.periodic}',
                timezone='Antarctica/Troll'
            ),
            task='app_habits.tasks.send_habit_notification',
            args=f'[{habit.id},{self.telegram_user.telegram_user_id}]'
        )

        url = reverse('api:habits-start', args=[habit.pk])

        self.client.post(
            path=url,
            data={"timezone": "Antarctica/Troll"},
            content_type="application/json"
        )

        self.assertEqual(send_telegram_message.call_count, 0)

    @patch('app_telegrambot.tasks.send_telegram_message.delay')
    def test_stop_notification_success(self, send_telegram_message: MagicMock):
        habit = self.non_public_habit

        PeriodicTask.objects.create(
            name=HabitViewSet.get_task_name(
                habit_id=habit.id,
                tg_user_id=self.telegram_user.telegram_user_id,
            ),
            crontab=CrontabSchedule.objects.create()
        )

        self.start_stop_notifications(send_telegram_message, False)

    def test_start_notifications_without_telegram_account_failed(self):
        habit = self.non_general_user_owner_habit_1

        self.client.force_login(self.general_user)

        url = reverse('api:habits-start', args=[habit.pk])
        response = self.client.post(
            path=url,
            data={"timezone": "Antarctica/Troll"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
