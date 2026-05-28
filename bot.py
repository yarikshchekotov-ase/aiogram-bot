from handlers.start import router as start_router
from handlers.ai_logic import ai_router
from handlers.audio import audio_router
from handlers.qr_code import qr_router
from handlers.random_int import ran_int_router
from handlers.currency import cur_router
from handlers.admin import admin_router
import asyncio
from aiogram import Bot, Dispatcher
import logging
from config import TOKEN
from aiogram import Bot
from aiohttp import ClientTimeout


# импорт библеотек 

timeout = ClientTimeout(
    total=60,      
    connect=30,    
    sock_read=30, 
    sock_connect=30
)

dp = Dispatcher()
# инициализация Диспечера
routers = [start_router, ai_router, qr_router, audio_router, ran_int_router, cur_router, admin_router]
for router in routers:
    dp.include_router(router) 


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

try:
    if __name__ == '__main__':
        # запуск бота и устанока логов
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] | [%(asctime)s] | %(name)s | %(message)s")
        asyncio.run(main())
except KeyboardInterrupt:
    logging.info('Завершение выполнения программы')
except Exception as e:
    logging.exception(f"____ Error: {e}____")

