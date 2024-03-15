import telebot
from telebot.types import Message, BotCommand


def init_cmd(bot: telebot.TeleBot):
    @bot.message_handler(commands=['cancel'], state='*')
    def cancel_command_handler(message: Message):
        uid = message.from_user.id
        cid = message.chat.id

        curr_state = bot.get_state(
            user_id=uid,
            chat_id=cid
        )

        if curr_state:
            with bot.retrieve_data(user_id=uid, chat_id=cid) as storage:
                storage.clear()

            bot.delete_state(
                user_id=uid,
                chat_id=cid
            )

            bot.send_message(
                chat_id=cid,
                text='Команда отменена'
            )
        else:
            bot.send_message(
                chat_id=cid,
                text='Команды не выполняются'
            )

    return BotCommand(
        command='cancel',
        description='Остановить выполнение команды'
    )
