import os
from loguru import logger

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CURRENCY = os.getenv('CURRENCY')
    LOCALE = os.getenv('LOCALE')
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')
    DATABASE_NAME = os.getenv('DATABASE_NAME')

mylogger =  logger.add('logs/debug.log', format='{time} {level} {message}', level='DEBUG', rotation='100 KB', compression='zip')
