import logging
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher import FSMContext

import tgbot.data.messages as messages
import tgbot.data.reply_commands as commands
import tgbot.keyboards.reply as reply_keyboards
from tgbot.services.db.database import Database


logger = logging.getLogger(__name__)

async def close(call: CallbackQuery):
    try:
        await call.message.delete()
        await call.answer()
    except MessageCantBeDeleted:
        await call.answer(text=messages.message_cant_be_deleted_error, show_alert=True)
        
        
async def block_check(chat_member: ChatMemberUpdated):
    users_worker = Database.get_users_worker()
    
    status = chat_member.new_chat_member.status
    if status == "kicked":
        is_blocked = True
        logger.info(f"User {chat_member.from_user.first_name} ({chat_member.from_user.id}) was blocked bot")
    elif status == "member":
        is_blocked = False
        logger.info(f"User {chat_member.from_user.first_name} ({chat_member.from_user.id}) was returned")
    else:
        logger.error(f"Unknown status of chat_member: {status}")
        return
        
    await users_worker.update_is_blocked(chat_member.from_user.id, is_blocked)
    
    
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.edit_reply_markup(reply_keyboards.main_keyboard)
    

def register_other(dp: Dispatcher):
    dp.register_callback_query_handler(close, text="close")
    dp.register_my_chat_member_handler(block_check)
    dp.register_message_handler(cancel, regexp=commands.cancel)
