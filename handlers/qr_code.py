import qrcode
import logging
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from forms.FSM import User
from aiogram import F
from keyboards import get_inline_keyboard, get_reply_keyboard
import io 
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery
import os
import validators
qr_router = Router()



@qr_router.callback_query(lambda c: c.data == 'QR')
async def audio(callback: CallbackQuery, state: FSMContext):
    message = await callback.message.answer('Введите URL-адрес: ')
    await state.update_data(message_id_qr_delete=message.message_id)
    await state.set_state(User.qr_url)
    await callback.answer()


@qr_router.message(User.qr_url, F.text)
async def qr_create(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('message_id_qr_delete')
    if msg_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    check_site = message.text
    if validators.url(check_site): # проверка правильность url-адреса
            img = qrcode.make(check_site)
            img.save('qr_code.png')
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            file = BufferedInputFile(buffer.read(), filename='qr_code.png')
            await message.answer_photo(photo=file, reply_markup=get_reply_keyboard())
            os.remove("qr_code.png")
            await message.delete()
            await state.clear()
    elif check_site.lower() == 'отмена':
        await message.answer("Привет я твой тг-бот!", reply_markup=get_inline_keyboard())
    else:
        logging.error("Ошибка")
        await message.answer("Неверный url-адрес!😯\nПопробуйте еще раз!🤗")