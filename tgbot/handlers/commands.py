import logging
from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.db.database import Database
import tgbot.keyboards.reply as reply_keyboards
import tgbot.data.messages as messages


logger = logging.getLogger(__name__)

async def start_command(message: Message):
    logger.info(f"User {message.from_user.first_name} ({message.from_user.id}) use /start")
    users_worker = Database.get_users_worker()
    
    is_user_exists = await users_worker.is_user_exists(message.from_user.id)
    if not is_user_exists:
        await users_worker.add_new_user(message.from_user.id)
        logger.info(f"User {message.from_user.first_name} ({message.from_user.id}) registred")
        
    await message.answer(messages.welcome_message, reply_markup=reply_keyboards.main_keyboard)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"], state="*")
