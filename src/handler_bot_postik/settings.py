import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_HANDLER_TOKEN')
API_URL = os.getenv('API_URL')
