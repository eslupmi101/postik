import os

import asyncio
import sys
import logging

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

TOKEN = os.getenv('BOT_MANAGER_TOKEN')
API_URL = os.getenv('API_URL')
BOT_MANAGER_ACCESS_TOKEN = os.getenv('BOT_MANAGER_ACCESS_TOKEN')

dp = Dispatcher()


async def send_auth_request(
    session_id: str,
    telegram_id: str,
    username: str
) -> tuple[str, dict]:
    """Send auth or registration request to backend api."""
    headers = {
        'Bot-Token': BOT_MANAGER_ACCESS_TOKEN
    }
    payload = {
        'session_id': session_id,
        'telegram_id': telegram_id,
        'username': username
    }
    async with aiohttp.ClientSession() as session:
        url = f'{API_URL}/api/v1/auth/bot_manager/'
        async with session.post(url, json=payload, headers=headers) as response:
            status = str(response.status)
            # if response does not contain json
            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                data = {}
            return status, data


@dp.message(CommandStart(deep_link=True))
async def auth_handler(message: Message, command: CommandObject):
    """Auth users from Postik."""
    args = command.args

    try:
        status, data = await send_auth_request(
            args,
            message.from_user.id,
            message.from_user.username,
        )
    except ConnectionError as e:
        logger.critical('Error connection to auth api. Error: %s', e)
        await message.answer('Технические работы')
        return

    if status not in ['200', '201']:
        logger.critical('Error sending auth request. Status: %s. Data: %s', status, data)
        await message.answer('Технические работы')
        return

    answer_messages = {
        '200': 'Вы успешно aвторизировались, перейдите на сайт',
        '201': 'Вы успешно зарегистрировались, перейдите на сайт'
    }

    await message.answer(answer_messages[status])


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
