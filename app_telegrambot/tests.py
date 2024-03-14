from django.test import TestCase
from django.test import override_settings
from app_telegrambot import message_text


class MessageTextTestCase(TestCase):

    def test_stack(self):
        msg = message_text.stack('line1', 'line2\nline3')
        self.assertEqual(msg, "line1\nline2\nline3")

    @override_settings(APPLICATION_HOSTNAME='example.com')
    @override_settings(APPLICATION_SCHEME='https')
    def test_message_welcome(self):
        msg = message_text.message_welcome()
        self.assertEqual(msg, "Вы зарегистрировались на сайте [example.com](https://example.com)")

    def test_message_user_credentials(self):
        msg = message_text.message_user_credentials('user1', 'pass')
        self.assertEqual(msg, "Для входа используйте:\n>Логин: `user1`\n>Пароль: ||pass||")
