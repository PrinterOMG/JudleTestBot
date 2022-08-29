import logging
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import tgbot.data.reply_commands as commands
import tgbot.data.messages as messages
import tgbot.keyboards.inline as inline_keyboards
from tgbot.services.db.database import Database
from tgbot.misc.states import PersonalInfoState


logger = logging.getLogger(__name__)

async def send_profile_message(message: Message):
    logger.info(f"User {message.from_user.first_name} ({message.from_user.id}) press '{commands.profile}'")
    personal_info_worker = Database.get_personal_info_worker()
    
    is_have_profile = personal_info_worker.is_user_have_personal_info(message.from_user.id)
    if is_have_profile:
        personal_info = personal_info_worker.get_user_personal_info(message.from_user.id)
        text = messages.profile_message.format(**personal_info)
        await message.answer(text)
    else:
        await message.answer(messages.personal_info_input_start_message, reply_markup=inline_keyboards.personal_info_confirm)
    

async def send_help_message(message: Message):
    logger.info(f"User {message.from_user.first_name} ({message.from_user.id}) press '{commands.help}'")
    
    await message.answer(text=messages.help_message)
    
    
async def send_work_message(message: Message):
    logger.info(f"User {message.from_user.first_name} ({message.from_user.id}) press '{commands.work}'")
    
    
async def send_store_message(message: Message):
    logger.info(f"User {message.from_user.first_name} ({message.from_user.id}) press '{commands.store}'")


def register_main_menu(dp: Dispatcher):
    dp.register_message_handler(send_profile_message, regexp=commands.profile)
    dp.register_message_handler(send_help_message, regexp=commands.help)
    dp.register_message_handler(send_work_message, regexp=commands.work)
    dp.register_message_handler(send_store_message, regexp=commands.store)
    
    