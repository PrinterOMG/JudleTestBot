import logging
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import tgbot.keyboards.reply as reply_keyboards
import tgbot.keyboards.inline as inline_keyboards
import tgbot.data.messages as messages
from tgbot.services.db.database import Database
from tgbot.misc.states import PersonalInfoState


logger = logging.getLogger(__name__)


async def start_personal_info_input(call: CallbackQuery, state: FSMContext):
    msg = await call.message.answer(messages.personal_info_name_input, reply_markup=reply_keyboards.cancel_keyboard)
    
    await state.update_data(msg=msg)
    await PersonalInfoState.waiting_for_name.set()
    
    await call.answer(show_alert=True, text="Сейчас начнётся заполнение профиля.\nДля отменты нажмите кнопку 'Отмена'.")
    

async def name_input(message: Message, state: FSMContext):
    async with state.proxy() as data:
        msg: Message = data["msg"]
        
        name = message.text
        if not name:
            text = ""
        else:
            text = ""
            data["name"] = name
            await PersonalInfoState.next()
    
    await message.delete()
    await msg.edit_text(text=text, reply_markup=reply_keyboards.cancel_keyboard)


async def age_input(message: Message, state: FSMContext):
    async with state.proxy() as data:
        msg: Message = data["msg"]
        
        age: str = message.text
        if not age.isdigit():
            text = ""
        elif int(age) not in range(10, 100):
            text = ""
        else:
            text = ""
            data["age"] = age
            await PersonalInfoState.next()
            
    await message.delete()
    await msg.edit_text(text=text, reply_markup=reply_keyboards.cancel_keyboard)


async def city_input(message: Message, state: FSMContext):
    async with state.proxy() as data:
        msg: Message = data["msg"]
        
        city = message.text
        if not city:
            text = ""
            keyboard = reply_keyboards.cancel_keyboard
        else:
            text = ""
            keyboard = reply_keyboards.phone_keyboard
            data["city"] = city
            await PersonalInfoState.next()
            
    await message.delete()
    await msg.edit_text(text=text, reply_markup=keyboard)


async def phone_input(message: Message, state: FSMContext):
    async with state.proxy() as data:
        msg: Message = data["msg"]
        
        phone: str = message.text
        if not phone:
            text = ""
            keyboard = reply_keyboards.cancel_keyboard
        else:
            phone = phone.replace("+", "").replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
            if phone.startswith("8"):
                phone = phone.replace("8", "7", count=1)
            
            if len(phone) != 11 or not phone.startswith("7"):
                text = ""
                keyboard = reply_keyboards.cancel_keyboard
            else:
                text = ""
                keyboard = inline_keyboards.profile_keyboard
                PersonalInfoWorker = Database.get_personal_info_worker()
                await PersonalInfoWorker.add_personal_info(message.from_user.id, data["name"], data["age"], data["city"], phone)
    
    await state.finish()
    await message.delete()
    await msg.edit_text(text=text, reply_markup=keyboard)
                

async def get_phone(message: Message, state: FSMContext):
    print(message.contact.phone_number)
    async with state.proxy() as data:
        msg: Message = data["msg"]
        
        PersonalInfoWorker = Database.get_personal_info_worker()
        await PersonalInfoWorker.add_personal_info(message.from_user.id, data["name"], data["age"], data["city"], message.contact.phone_number)
    
    await state.finish()
    await message.delete()
    await msg.edit_text(text=text, reply_markup=inline_keyboards.profile_keyboard)
        

def register_personal_info(dp: Dispatcher):
    dp.register_callback_query_handler(start_personal_info_input, text="personal_info_confirm")
    
    dp.register_message_handler(name_input, state=PersonalInfoState.waiting_for_name)
    dp.register_message_handler(age_input, state=PersonalInfoState.waiting_for_age)
    dp.register_message_handler(city_input, state=PersonalInfoState.waiting_for_city)
    dp.register_message_handler(phone_input, state=PersonalInfoState.waiting_for_phone)
    dp.register_message_handler(get_phone, state=PersonalInfoState.waiting_for_phone, content_types=["contact"])
