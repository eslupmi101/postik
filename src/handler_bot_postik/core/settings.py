import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_HANDLER_TOKEN')
BOT_MANAGER_TOKEN = os.getenv('BOT_MANAGER_TOKEN')
CHANNEL_DEVELOP_ID = os.getenv('CHANNEL_DEVELOP_ID')
API_URL = os.getenv('API_URL')
BOT_HANDLER_ACCESS_TOKEN = os.getenv('BOT_HANDLER_ACCESS_TOKEN')

# Database
HOST_DATABASE = os.getenv('MONGODB_HOST', 'localhost')
PORT_DATABASE = os.getenv('MONGODB_PORT', '27017')
USERNAME_DATABASE = os.getenv('MONGODB_USERNAME')
PASSWORD_DATABASE = os.getenv('MONGODB_PASSWORD')

NAME_DATABASE = os.getenv('MONGODB_NAME', 'postik')
NAME_COLLECTION = 'posts'

MINIO_URI: str = (
    f'mongodb://{USERNAME_DATABASE}:{PASSWORD_DATABASE}@{HOST_DATABASE}:{PORT_DATABASE}'
)
