import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramUnauthorizedError
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

logger = logging.getLogger(__name__)


async def get_message_log_info(message: Message) -> str:
    return (
        f'Message id: {message.message_id}, '
        f'user_id: {message.from_user.id}, '
        f'data: {message.date}.'
    )
