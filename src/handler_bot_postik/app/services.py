from bson.objectid import ObjectId
import logging
from typing import Dict, List, Tuple

import aiohttp
from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.serialization import deserialize_telegram_object_to_python
from aiogram.utils.media_group import MediaGroupBuilder
from pymongo.errors import PyMongoError

from app.utils import get_message_log_info
from core.database import col
from core.settings import API_URL, BOT_HANDLER_ACCESS_TOKEN

logger = logging.getLogger(__name__)


async def send_post_to_api(telegram_id: int, message_id: int) -> tuple[int, dict]:
    headers = {
        'Bot-Token': BOT_HANDLER_ACCESS_TOKEN
    }
    payload = {
        'telegram_id': telegram_id,
        'message_id': message_id
    }
    try:
        async with aiohttp.ClientSession() as session:
            url = f'{API_URL}/api/v1/posts/'
            async with session.post(url, json=payload, headers=headers) as response:
                try:
                    data = await response.json()
                except aiohttp.ContentTypeError:
                    data = {}
                return response.status, data
    except aiohttp.ClientError as e:
        logger.error(f'Cannot send post to API. {e}')
        return 0, {}


async def get_purchased_posts(telegram_id: int) -> Tuple[int, List[Dict]]:
    headers = {
        'Bot-Token': BOT_HANDLER_ACCESS_TOKEN,
        'telegram-id': str(telegram_id)
    }
    async with aiohttp.ClientSession() as session:
        url = f'{API_URL}/api/v1/posts/purchase/'
        async with session.get(url, headers=headers) as response:
            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                data = []

            return response.status, data


async def get_post_details(telegram_id: int, post_id: int) -> Tuple[int, Dict]:
    headers = {
        'Bot-Token': BOT_HANDLER_ACCESS_TOKEN,
        'telegram-id': str(telegram_id)
    }
    async with aiohttp.ClientSession() as session:
        url = f'{API_URL}/api/v1/posts/purchase/{post_id}/'
        async with session.get(url, headers=headers) as response:
            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                data = {}
            return response.status, data


async def save_message_post(message: Message) -> str | None:
    """
    Saves a message to MongoDB and returns the ObjectId of the document.

    Args:
    message (Message): The message object to be saved.

    Returns:
    str | None: The ObjectId of the saved message as a string if the save is successful,
                otherwise None.

    Exceptions:
    PyMongoError: Handles all errors related to MongoDB operations.
                  This includes connection errors, data insertion errors,
                  and other database-related operations.
    """
    try:
        message_dict = dict(deserialize_telegram_object_to_python(message))
        message_dict['is_media_group'] = False
        result = await col.insert_one(message_dict)
        return str(result.inserted_id)
    except PyMongoError as e:
        logger.critical(
            'Error with saving message-post to MongoDB - %s: %s',
            get_message_log_info(message), e
        )


async def save_media_group_post(message: Message, album: List[Message]) -> str | None:
    try:
        message_dict = {
            'media_group': [dict(deserialize_telegram_object_to_python(m)) for m in album],
            'is_media_group': True,
            'caption': album[0].caption
        }
        result = await col.insert_one(message_dict)
        return str(result.inserted_id)
    except PyMongoError as e:
        logger.critical(
            'Error with saving message-post to MongoDB - %s: %s',
            get_message_log_info(message), e
        )


async def send_post_user(bot: Bot, user_id: str, post_details: dict[str]):
    message_obj = await col.find_one(
        {'_id': ObjectId(post_details['message_id'])}
    )

    if not message_obj['is_media_group']:
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=post_details['telegram_id'],
            message_id=message_obj['message_id']
        )
    else:
        media_group = MediaGroupBuilder(caption=message_obj['caption'])
        for media in message_obj['media_group']:
            if 'photo' in media:
                media_group.add(
                    type='photo',
                    media=media['photo'][-1]['file_id'],
                )
            if 'video' in media:
                media_group.add(
                    type='video',
                    media=media['video'][-1]['file_id'],
                )
            if 'audio' in media:
                media_group.add(
                    type='audio',
                    media=media['audio'][-1]['file_id'],
                )
            if 'document' in media:
                media_group.add(
                    type='document',
                    media=media['document'][-1]['file_id'],
                )
        await bot.send_media_group(user_id, media=media_group.build())

    description = post_details.get('description', 'Описание отсутствует')
    price = post_details.get('price', 'Цена отсутствует')
    await bot.send_message(
        user_id,
        f"Название: {post_details['title']}\nОписание: {description}\nЦена: {price}"
    )
