from typing import Dict, List, Tuple

import aiohttp

from settings import API_URL, TOKEN


async def send_post_to_api(telegram_id: int, message_id: int) -> tuple[str, dict]:
    headers = {
        'Bot-Token': TOKEN
    }
    payload = {
        'telegram_id': telegram_id,
        'message_id': message_id
    }
    async with aiohttp.ClientSession() as session:
        url = f'{API_URL}/api/v1/posts/'
        async with session.post(url, json=payload, headers=headers) as response:
            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                data = {}
            return response.status, data


async def get_purchased_posts(telegram_id: int) -> Tuple[int, List[Dict]]:
    headers = {
        'Bot-Token': TOKEN,
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
        'Bot-Token': TOKEN,
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
