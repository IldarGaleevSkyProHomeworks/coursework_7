import telebot
from telebot.formatting import escape_markdown
from telebot.types import Message

from app_telegrambot.models import TelegramUser


def init_cmd(bot: telebot.TeleBot):
    @bot.message_handler(commands=['start'])
    def start_command_handler(message: Message):
        uid = message.from_user.id
        accounts = TelegramUser.objects.filter(telegram_user_id=uid)

        if accounts.exists():
            bot.send_message(
                chat_id=uid,
                parse_mode='MarkdownV2',
                text=escape_markdown("Ой! А я вас знаю, вот ваши аккаунты:\n\n" +
                                     "\n".join([f'- `{account.user.username}`' for account in accounts])
                                     )
            )
        else:
            bot.send_message(
                chat_id=uid,
                parse_mode='MarkdownV2',
                text=escape_markdown("Давай знакомиться! Для этого вызови одну из комманд:\n\n"
                                     "- /link - чтобы привязать существующий аккаунт\n"
                                     "- /create - чтобы создать новый аккаунт\n"
                                     )
            )
