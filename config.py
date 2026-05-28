from dotenv import load_dotenv
from os import getenv
import logging
'''файл для устаноки не изменяемых переменных: такие как ключ-бота, ключ-нейросети и устанока формата логов'''
load_dotenv() # читаем API из файла .env
TOKEN = getenv('TOKEN')
OPENROUTER_KEY = getenv('OPENROUTER_KEY')
CURRENCY_KEY = getenv('CURRENCY_KEY')
ADMIN_ID = int(getenv('ADMIN_ID'))
GROUP_ID = int(getenv('GROUP_ID'))
PROXY = getenv('PROXY')