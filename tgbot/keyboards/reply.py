from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import tgbot.data.reply_commands as commands


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=commands.profile)
    ],
    [
        KeyboardButton(text=commands.work)
    ],
    [
        KeyboardButton(text=commands.store)
    ],
    [
        KeyboardButton(text=commands.help)
    ]
], resize_keyboard=True)

cancel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=commands.cancel)
    ]
])

phone_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Передать номер из Telegram", request_contact=True)
    ],
    [
        KeyboardButton(text=commands.cancel)
    ]
])
