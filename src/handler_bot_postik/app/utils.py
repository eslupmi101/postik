import logging

from aiogram.types import Message

logger = logging.getLogger(__name__)


async def get_message_log_info(message: Message) -> str:
    return (
        f'Message id: {message.message_id}, '
        f'user_id: {message.from_user.id}, '
        f'data: {message.date}.'
    )
