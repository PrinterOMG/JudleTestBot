from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


personal_info_confirm = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Начать заполнение профиля", callback_data="personal_info_confirm")
    ],
    [
        InlineKeyboardButton(text="Закрыть", callback_data="close")
    ]
])
