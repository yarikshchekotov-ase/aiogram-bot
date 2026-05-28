import asyncio
from openai import AsyncOpenAI, APIError, APIConnectionError
from config import OPENROUTER_KEY
from utils import split_message
from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery
import logging
from aiogram.types import Message
from forms.FSM import User
from keyboards import get_inline_keyboard, get_reply_keyboard
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY
)
ai_router = Router()

@ai_router.callback_query(lambda c: c.data == 'quesion')
async def question(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите вопрос: ')
    await state.set_state(User.ai_quesion)
    await callback.answer()

@ai_router.message(User.ai_quesion, F.text)
async def answer(message: Message, state: FSMContext, bot: Bot):
    question = message.text
    if question.lower() == 'отмена':
            await state.clear()
            await message.answer('Вот как я могу тебе помочь',reply_markup=get_inline_keyboard())
    else:
        await state.update_data(question=message.text)
        data = await state.get_data()
        question = data.get('question')
        try:
            async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
                    logging.info("Обработка сообщения")
                    response = await client.chat.completions.create(
                        model="liquid/lfm-2.5-1.2b-instruct:free",
                        messages=[{"role": "user", "content": question}],
                        temperature=0.7,
                        extra_headers={
                            "HTTP-Referer": "t.me/JOhn1890_bot",
                            "X-Title": "Telegram AI Bot"
                        }
                    )
                    res = response.choices[0].message.content
                    if response and response.choices:
                        res = response.choices[0].message.content
                    else:
                        res = "Произошла ошибка: модель прислала пустой ответ."
            if len(res)>4000:
                    parts = split_message(res)
                    for part in parts:
                        await message.answer(part)
            else:
                logging.info('Отправил сообщение')
                await message.answer(res, reply_markup=get_reply_keyboard())
            await state.clear()
        except APIConnectionError as e:
            logging.error(f"____ Ошибка соединения: {e} ____")
            await message.answer('Проблема с подключением. Проверьте интернет.')
        except APIError as e:
            logging.error(f"____ Ошибка соединения с API модели: {e} ____")
            await message.answer('Ошибка нейросеть недоступна!!!\nПопробуйте позже!!!')
        except Exception as e:
            logging.exception(f'____ Ошибка: {e} ____')
            await message.answer('Что-то пошло не так')



