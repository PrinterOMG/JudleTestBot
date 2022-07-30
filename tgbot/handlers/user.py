import logging
from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.db.database import Database

async def user_start(message: Message):
    logger = logging.getLogger(__name__)
    users_worker = Database.get_users_worker()
    
    is_user_exists = await users_worker.is_user_exists(message.from_user.id)
    if not is_user_exists:
        await users_worker.add_new_user(message.from_user.id)
        logger.info(f"User {message.from_user.first_name} ({message.from_user.id}) registred")
        
    await message.answer("Hello, user!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
