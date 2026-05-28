from aiogram.types import Message
from aiogram import Router, Bot
from aiogram.filters import Command
from keyboards import get_reply_keyboard, get_inline_keyboard, admin_panel
from config import ADMIN_ID
router = Router()

@router.message(Command('start', 'info'))
async def start(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"Здраствуйте, {message.from_user.first_name} вы вошли как админ бота!\n<i>Доступные опции:</i>", reply_markup=admin_panel(), parse_mode='HTML')
    else:
        await message.answer('Привет я твой тг-бот', reply_markup=get_reply_keyboard())


@router.message(Command('help'))
async def help(message:Message):
    await message.answer('<b>Вот как я могу тебе помочь!</b>',reply_markup=get_inline_keyboard(), parse_mode='HTML')


