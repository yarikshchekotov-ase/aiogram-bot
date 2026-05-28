from config import CURRENCY_KEY
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards import currency_keyboard as ck
from keyboards import get_reply_keyboard as grk
from forms.FSM import User
import logging
from utils import validator_currency as val_cur
import aiohttp
cur_router= Router()


@cur_router.callback_query(lambda c: c.data == 'currency')
async def money(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите сумму:')
    await state.set_state(User.money)
    await callback.answer()
    

@cur_router.message(User.money, F.text)
async def first_currency(message: Message, state: FSMContext):
    await state.update_data(money=message.text)
    await message.answer('Из какой валюты перевести: ', reply_markup=ck())
    await state.set_state(User.cur_1)


@cur_router.message(User.cur_1, F.text)
async def second_currency(message: Message, state: FSMContext):
    await state.update_data(cur_1=message.text)
    await message.answer("В какую валюту перевести: ", reply_markup=ck())
    await state.set_state(User.cur_2)

@cur_router.message(User.cur_2, F.text)
async def final(message: Message, state: FSMContext):
    await state.update_data(cur_2=message.text)
    data = await state.get_data()
    money = data.get('money')
    first_cur = data.get('cur_1')
    first_cur = val_cur(first_cur)
    second_cur = data.get('cur_2')
    second_cur = val_cur(second_cur)
    try:
        url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_KEY}/pair/{first_cur}/{second_cur}/{money}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data_cur = await response.json()
                    otv = data_cur["conversion_result"]
                    await message.answer(f"Результат: {otv}", reply_markup=grk())
                    await state.clear()
                else:
                    logging.info(f'Ошибка номер: {response.status}')
                    await message.answer(f'Ошибка:{response.status}')
    except Exception as e:
        logging.info(f'Ошибка:{e}')
        await message.answer("Ошибка попробуйте снова", reply_markup=grk())