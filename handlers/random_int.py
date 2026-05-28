from forms.FSM import User
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import random
from aiogram import Router, F
import logging
from keyboards import get_inline_keyboard
ran_int_router = Router()



@ran_int_router.callback_query(lambda c: c.data == 'random_int')
async def first_int(callback: CallbackQuery, state: FSMContext):
    try:
        message = await callback.message.answer('Введите первое число:')
        await state.update_data(message_id_int_to_delete=message.message_id)
        await state.set_state(User.first_int)
        await callback.answer() 
    except ValueError:
        await callback.message.answer('Вы ввели не число\n\nВведите число!')

@ran_int_router.message(User.first_int, F.text)
async def second_int(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer("Привет я твой тг-бот!", reply_markup=get_inline_keyboard())
    else:    
        try:
            await state.update_data(first_int=int(message.text))
            data = await state.get_data()
            msg_id = data.get('message_id_int_to_delete')
            if msg_id:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
            await message.delete()
            message = await message.answer('Введите второе число:')
            await state.update_data(message_id_int_to_delete=message.message_id)
            await state.set_state(User.second_int)
        except ValueError:
            logging.error("Ошибка")
            await message.answer('Вы ввели не число\n\nВведите число!')
            
@ran_int_router.message(User.second_int, F.text)
async def final(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer("Привет я твой тг-бот!", reply_markup=get_inline_keyboard())
    else:
        try:
            await state.update_data(second_int=int(message.text))
            data = await state.get_data()
            msg_id = data.get('message_id_int_to_delete')
            if msg_id:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
            first_num = data.get("first_int")
            second_num = data.get("second_int")
            await message.delete()
            if  first_num > second_num:
                num = random.randint(second_num ,first_num)
                await message.answer(f'Сгенерировано число: {num}!')
                await state.clear()
            else:
                num = random.randint(first_num, second_num)
                await message.answer(f'Сгенерировано число: {num}!')
                await state.clear()
        except ValueError:
            await message.answer('Вы ввели не число\n\nВведите число!')