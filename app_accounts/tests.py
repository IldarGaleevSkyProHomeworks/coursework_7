from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UserAccountsTestCase(TestCase):
    def test_user_create_success(self):
        test_data = {
            'password': '123',
            'username': 'user1'
        }
        url = reverse('accounts:users-list')
        response = self.client.post(url, data=test_data)
        result = response.json()

        username = result['username']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(username, 'user1')

    def test_user_update_full_success(self):
        user: User = User.objects.create_user(username='test_user', password='123')
        user.first_name = 'Old first name'
        user.last_name = 'Old last name'
        user.save()

        self.client.force_login(user)

        test_data = {
            'first_name': 'New first name',
            'last_name': 'New last name'
        }

        url = reverse('accounts:users-detail', args=[user.pk])
        response = self.client.patch(
            url,
            data=test_data,
            content_type="application/json"
        )

        result = response.json()

        first_name = result['first_name']
        last_name = result['last_name']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(first_name, 'New first name')
        self.assertEqual(last_name, 'New last name')

    def partial_update(self, user, field, value):
        self.client.force_login(user)

        test_data = {
            field: value
        }

        url = reverse('accounts:users-detail', args=[user.pk])
        response = self.client.patch(
            url,
            data=test_data,
            content_type="application/json"
        )

        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return result

    def test_user_update_partial_full_success(self):
        user: User = User.objects.create_user(username='test_user', password='123')
        user.first_name = 'Fn'
        user.last_name = 'Ln'
        user.save()

        result = self.partial_update(user, 'first_name', 'newFn')

        self.assertEqual(result['first_name'], 'newFn')
        self.assertEqual(result['last_name'], 'Ln')

        result = self.partial_update(user, 'last_name', 'newLn')

        self.assertEqual(result['first_name'], 'newFn')
        self.assertEqual(result['last_name'], 'newLn')

    def test_user_update_same_forbidden(self):
        same_user: User = User.objects.create_user(username='test_user_1', password='123')
        user: User = User.objects.create_user(username='test_user', password='123')
        user.first_name = 'Old first name'
        user.save()

        self.client.force_login(same_user)

        test_data = {
            'first_name': 'New first name'
        }

        url = reverse('accounts:users-detail', args=[user.pk])
        response = self.client.patch(
            url,
            data=test_data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_by_superuser_success(self):
        admin = User.objects.create_superuser(username='admin', password='123')
        user: User = User.objects.create_user(username='test_user', password='123')

        self.client.force_login(admin)

        url = reverse('accounts:users-detail', args=[user.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_delete_by_generic_user_forbidden(self):
        generic_user = User.objects.create_user(username='generic_user', password='123')
        user: User = User.objects.create_user(username='test_user', password='123')

        self.client.force_login(generic_user)

        url = reverse('accounts:users-detail', args=[user.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_self_forbidden(self):
        user: User = User.objects.create_user(username='test_user', password='123')

        self.client.force_login(user)

        url = reverse('accounts:users-detail', args=[user.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
