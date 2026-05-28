from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_reply_keyboard():
    keyboard_create = [
                '/help',
                '/info'
        ]
    keyboard= ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t)] for t in keyboard_create
        ],
        resize_keyboard=True
    )
    return keyboard


def get_inline_keyboard():
    keyboard_create = {
                "Записать аудио": 'audio',
                'Задать вопрос': 'quesion',
                'Сгенерировать число': 'random_int',
                'Создать QR-код': 'QR',
                'Записать заметку': 'write_notes',
                'Перевести валюту': 'currency'
            }
    
    buttons = [[InlineKeyboardButton(text=t, callback_data=cb)] for t, cb in keyboard_create.items()]
    buttons.append([InlineKeyboardButton(text='Служба поддержки', callback_data='help', style='success')])
    keyboard= InlineKeyboardMarkup(
        inline_keyboard=buttons
    ) 
    return keyboard


def currency_keyboard():
    keyboard_create = [
                '🇷🇺',
                '🇺🇸',
                '🇪🇺',
                '🇬🇧'
        ]
    keyboard= ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t)] for t in keyboard_create
        ],
        resize_keyboard=True
    )
    return keyboard

def admin_panel():
    keyboard_create = {
                "Панель администратора": 'admin'
            }
    keyboard= InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t, callback_data=cb)] for t, cb in keyboard_create.items()
        ]
    )
    return keyboard

async def admin_options():
    keyboard_create = [
                '/рассылка',
                '/kick_user'
        ]
    keyboard= ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t)] for t in keyboard_create
        ],
        resize_keyboard=True
    )
    return keyboard