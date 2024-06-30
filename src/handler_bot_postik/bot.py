import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from settings import TOKEN
from services import get_post_details, get_purchased_posts, send_post_to_api
from utils import send_post_message


MAIN_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить пост')],
        [KeyboardButton(text='Посмотреть посты')]
    ],
    resize_keyboard=True
)

dp = Dispatcher(storage=MemoryStorage())


class PostStates(StatesGroup):
    sending = State()


@dp.message(CommandStart(deep_link=True))
async def start_handler(message: types.Message, command: CommandObject):
    if len(command.args.split(',')):
        post_ids = command.args.split(',')

        for post_id in post_ids:
            status, post_details = await get_post_details(message.from_user.id, post_id)

            if status == 200:
                await send_post_message(
                    message.bot,
                    message.from_user.id,
                    post_details
                )
            else:
                await message.answer(
                    f'Не удалось получить детали для поста с ID: {post_id}'
                )

        await message.answer(
            'Привет, это Postik! Нажмите кнопку ниже, чтобы отправить или посмотреть купленные посты.',
            reply_markup=MAIN_KB
        )

    else:
        await message.answer(
            'Привет, это Postik! Нажмите кнопку ниже, чтобы отправить или посмотреть посты.',
            reply_markup=MAIN_KB
        )


@dp.message(F.text == 'Отправить пост')
async def process_post_message(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте ваше сообщение для поста.')
    await state.set_state(PostStates.sending)


@dp.message(PostStates.sending)
async def post_message_handler(message: types.Message, state: FSMContext):
    error_msg = 'Произошла ошибка при сохранении вашего поста. Пожалуйста, попробуйте снова.'
    try:
        status, data = await send_post_to_api(
            message.from_user.id,
            message.message_id
        )
        if status == 201:
            post_id = data['id']
            await message.answer(f'Ваш пост под номером {post_id} был успешно сохранен.')
        else:
            await message.answer(error_msg)
    except ConnectionError as e:
        logging.error('Cannot send post to backend. %s', e)
        await message.answer(error_msg)
    await state.clear()


@dp.message(F.text == 'Посмотреть посты')
async def view_posts_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    status, purchased_posts = await get_purchased_posts(telegram_id)

    if not purchased_posts or status != 200:
        await message.answer('У вас нет купленных постов.')
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=post['title'], callback_data=f"view_post_{post['id']}")]
        for post in purchased_posts
    ])

    await message.answer('Ваши купленные посты:', reply_markup=kb)


@dp.callback_query(lambda callback_query: callback_query.data.startswith('view_post_'))
async def view_post_details_handler(callback_query: types.CallbackQuery):
    telegram_id = callback_query.from_user.id
    post_id = int(callback_query.data.split('_')[2])
    status, post_details = await get_post_details(telegram_id, post_id)

    if not post_details or status != 200:
        await callback_query.message.answer('Произошла ошибка при получении деталей поста.')
        return

    await send_post_message(
        callback_query.bot,
        callback_query.from_user.id,
        post_details
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
