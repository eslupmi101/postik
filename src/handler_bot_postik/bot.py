import asyncio
import logging
import os
import sys

import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_HANDLER_TOKEN')

API_URL = os.getenv('API_URL')

MAIN_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить пост", callback_data="send_post")]
    ]
)

dp = Dispatcher(storage=MemoryStorage())


class PostStates(StatesGroup):
    sending = State()


async def send_post_to_api(
    telegram_id: int,
    message_id: int
) -> tuple[str, dict]:
    """Save post in main backend."""
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
            status = str(response.status)
            # if response does not contain json
            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                data = {}
            print(data)
            return status, data


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        'Привет, это Postik! Нажмите кнопку ниже, чтобы отправить пост.',
        reply_markup=MAIN_KB
    )


@dp.callback_query(F.data == 'send_post')
async def send_post_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Пожалуйста, отправьте ваше сообщение для поста.')
    await state.set_state(PostStates.sending)


@dp.message(PostStates.sending)
async def post_message_handler(message: types.Message, state: FSMContext):
    error_msg = 'Произошла ошибка при сохранении вашего поста. Пожалуйста, попробуйте снова.'
    try:
        status, data = await send_post_to_api(
            message.from_user.id,
            message.message_id
        )
        if status == '201':
            post_id = data['id']
            await message.answer(f'Ваш пост под номером {post_id} был успешно сохранен.')
        else:
            await message.answer(error_msg)
    except ConnectionError as e:
        logging.error('Cannot send post to backend. %s', e)
        await message.answer(error_msg)
    await state.clear()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
