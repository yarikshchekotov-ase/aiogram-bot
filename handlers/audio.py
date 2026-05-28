from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile
from forms.FSM import User
import logging 
from aiogram.utils.chat_action import ChatActionSender
from aiogram import F
import gtts
from keyboards import get_inline_keyboard, get_reply_keyboard
import os
import asyncio
from aiogram.fsm.context import FSMContext

audio_router = Router()
# создаем роутер 

@audio_router.callback_query(lambda c: c.data == 'audio')
async def qr_code(callback: CallbackQuery, state: FSMContext):
    '''отслеживаем нажатие кноки с помощю callback'''
    message = await callback.message.answer('Введите текст: ')
    await state.update_data(message_id_audio_delete=message.message_id)
    await state.set_state(User.audio_text) # сохраняем состояние
    await callback.answer() 

@audio_router.message(User.audio_text, F.text)
async def save_text(message: Message, state: FSMContext):
    await state.update_data(audio_text=message.text)
    data = await state.get_data()
    msg_id = data.get('message_id_audio_delete')
    if msg_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    await message.delete() 
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("Привет я твой тг-бот!", reply_markup=get_inline_keyboard())
    else:
        message = await message.answer('Введите язык(ru/en):')
        await state.update_data(message_id_audio_delete=message.message_id)
        await state.set_state(User.audio_lang)


@audio_router.message(User.audio_lang, F.text)
async def save_lang(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(audio_lang=message.text)
    data = await state.get_data()
    msg_id = data.get('message_id_audio_delete')
    if msg_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer("Привет я твой тг-бот!", reply_markup=get_inline_keyboard())
    else:
        try:
            await message.delete()
            await state.update_data(audio_lang=message.text)
            check_lang = message.text
            text = str(data.get('audio_text'))
            lang = str(data.get('audio_lang'))
            if check_lang.lower() == 'отмена':
                await message.answer("Привет я твой тг-бот!", reply_markup=get_inline_keyboard())
            else:
                tts = gtts.gTTS(text=text, lang=lang)
                tts.save('hello.mp3')
                audio_file = FSInputFile('hello.mp3')
                async with ChatActionSender.upload_voice(bot=bot, chat_id=message.chat.id):
                    await asyncio.sleep(5)
                    await message.answer_audio(audio=audio_file, reply_markup=get_reply_keyboard())
                os.remove('hello.mp3')
                await state.clear()
        except ValueError as e:
            logging.error(f'____ Ошибка: {e} ____')
            await message.answer("Ошибка введите правильный язык ru или en!🤗")
        except Exception as e:
            logging.exception(f"____ Ошибка:{e} ____")