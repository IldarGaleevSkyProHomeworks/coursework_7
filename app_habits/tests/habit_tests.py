from datetime import time

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from app_habits.models import Habit


class HabitTestCase(TestCase):

    def setUp(self):
        self.general_user_owner = User.objects.create_user(username='GeneralUserOwner', password='123')
        self.general_user = User.objects.create_user(username='GeneralUser', password='123')
        self.super_user = User.objects.create_superuser(username='SuperUser', password='123')

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
            "periodic": 0,
            "reward": "string",
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
            "periodic": 0,
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
            "periodic": 0,
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
            "periodic": 0,
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
            "periodic": 0,
            "duration": 500,
            "reward": "string",
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['duration'][0], 'Приятная привычка не должна длиться больше двух минут')

    def test_create_validation_pleasantly_habit_non_set_reward_failed(self):
        data = {
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": True,
            "periodic": 0,
            "duration": 0,
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['reward'][0], 'Укажите награду')

    def test_create_validation_non_pleasantly_habit_reward_and_linked_habit_not_set_failed(self):
        data = {
            "time": "10:00",
            "site": "string",
            "action_description": "string",
            "is_pleasantly": False,
            "periodic": 0,
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
            "periodic": 0,
            "duration": 0,
            "reward": "string",
            "is_public": True
        }

        _, result = self.check_create_habit(data, self.general_user_owner)

        self.assertEqual(result['linked_habit'][0], 'Если указана награда, связанную привычку указать нельзя')
        self.assertEqual(result['reward'][0], 'Если указана связанная привычка, награду указывать нельзя')
