from aiogram import Router, F
from aiogram.types import CallbackQuery, Message 
from aiogram.filters import Command
from keyboards import admin_options
from aiogram import Bot
from config import GROUP_ID, ADMIN_ID
from aiogram.fsm.context import FSMContext
admin_router = Router()


@admin_router.callback_query(lambda c: c.data == 'admin')
async def admin(callback: CallbackQuery):
    await callback.message.answer('<b><i>Выберите из что-то предложенных опций:</i></b>', reply_markup=admin_options(), parse_mode='HTML')


@admin_router.message(Command('рассылка'))
async def newsletter(message: Message, bot: Bot):
    await bot.send_message(int(ADMIN_ID), '<b>Привет, я Джон!</b>\n<b><i>Я помогу тебе если тебе надо!</i></b>\nОбращайся!!', parse_mode='HTML')
    await message.answer(f"<b><i>Отправил сообщения юзерам:\n@{message.from_user.username}</i></b>", parse_mode='HTML')


@admin_router.callback_query(lambda c: c.data == 'help')
async def question_for_admin(callback: CallbackQuery, state: FSMContext):
    message = await callback.message.answer('<b><i>Опишите вашу проблему:</i></b>', parse_mode='HTML')
    await state.update_data(message_for_admin_delete=message.message_id)
    await callback.answer() 


@admin_router.message()
async def for_admin(message: Message, state: FSMContext,  bot: Bot):
    # await bot.forward_message(
        # chat_id=int(GROUP_ID), 
        #from_chat_id=message.from_user.id, 
        #message_id=message.message_id
    # )
    await message.copy_to(GROUP_ID) # отправляет сообщение без перессылки, bot.forward_message() перессылает сообщение в группу
    await bot.send_message(GROUP_ID, f'Сообщение от: @{message.from_user.username}')
    data = await state.get_data()
    msg_id = data.get('message_for_admin_delete')
    if msg_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    await message.delete()
    await message.answer("<b><i>Сообщение было отправлено!!\nВ скором времени с вами свяжется служба поддержки!!</i></b>", parse_mode='HTML')
    await state.clear()