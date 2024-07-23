import asyncio
import logging
import os
import sys

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

TOKEN = os.getenv('BOT_MANAGER_TOKEN')
API_URL = os.getenv('API_URL')
BOT_MANAGER_ACCESS_TOKEN = os.getenv('BOT_MANAGER_ACCESS_TOKEN')

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


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


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Получить кнопку с ссылкой на карточку')],
            [KeyboardButton(text='Редактировать текст кнопки со ссылкой')],
        ],
        resize_keyboard=True
    )
    await message.answer(
        'Привет, это бот менеджер <b>POSTIK!</b>',
        reply_markup=keyboard
    )


@dp.message(F.text == 'Получить кнопку с ссылкой на карточку')
async def get_card_link_button(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    username = message.from_user.username
    data = await state.get_data()
    button_text = data.get('button_text')
    message_text = data.get('message_text')

    button_text = button_text if button_text else 'Мои посты 🚀'
    message_text = message_text if message_text else 'Вы можете купить мои платные посты здесь'

    builder.add(InlineKeyboardButton(
        text=button_text,
        url=f'https://postik.tech/cards/{username}/')
    )
    await message.answer(
        message_text,
        reply_markup=builder.as_markup()
    )


class EditTextStates(StatesGroup):
    waiting_for_button_text = State()
    waiting_for_message_text = State()


@dp.message(F.text == 'Редактировать текст кнопки со ссылкой')
async def edit_button_text(message: Message, state: FSMContext):
    await message.answer('Введите новый текст для кнопки:')
    await state.set_state(EditTextStates.waiting_for_button_text)


@dp.message(EditTextStates.waiting_for_button_text)
async def set_button_text(message: Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await message.answer('Текст кнопки обновлен. Введите новый текст для сообщения:')
    await state.set_state(EditTextStates.waiting_for_message_text)


@dp.message(EditTextStates.waiting_for_message_text)
async def set_message_text(message: Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    await message.answer('Кнопка с ссылкой сохранена!')
    await state.set_state(state=None)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
