import logging
import re

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.middlewares import AlbumMiddleware
from app.services import create_lead
from core.settings import BOT_MANAGER_TOKEN, TOKEN

logger = logging.getLogger(__name__)

bot_manager = Bot(token=BOT_MANAGER_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

MAIN_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Создать новый пост')],
        [KeyboardButton(text='Посмотреть посты')]
    ],
    resize_keyboard=True
)

dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(AlbumMiddleware())


class PostStates(StatesGroup):
    sending = State()


@dp.message(CommandStart(deep_link=True))
async def start_handler_purchased_posts(message: types.Message, command: CommandObject, bot: Bot):
    if lead_create_match := re.match(r"lead_create_(\d+)", command.args):
        post_id = lead_create_match.group(1)
        status, data = await create_lead(int(post_id), message.from_user.username, message.from_user.id)

        if status == 201:
            logger.debug('Create lead of post %s: %s. %s', post_id, status, data)
            post_title = data['post_details']['title']
            post_price = data['post_details']['price']
            post_description = data['post_details']['description']
            lead_id = data['id']

            await message.answer(
                'Привет, это Postik!\n'
                f'Заявка №{lead_id} на покупку поста создана\n\n'
                f'<b>{post_title} {post_price}₽</b>\n'
                f'{post_description}'
            )

            # Отправка лида владельцу
            sibscriber_username = data['subscriber_username']
            message_to_subscriber = (
                f'Заявка №{lead_id} на покупку поста создана\n'
                f'<b>{post_title} {post_price}₽</b>\n'
                f'Покупатель: {sibscriber_username}'
            )
            await bot_manager.send_message(
                data['author_telegram_id'],
                message_to_subscriber
            )
            return

        logger.critical('Cannot create lead of post %s: %s. %s', post_id, status, data)
        await message.answer(
            'Проводятся технические работы =('
        )

    #     # Create post event
    #     if command.args == 'create_post':
    #     await message.answer(
    #         'Чтобы создать пост, отправьте одно сообщение или перешлите сюда сообщение'
    #     )
    #     await state.set_state(PostStates.sending)
    #     return

    # if view_post_match := re.match(r"view_post_(\d+)", command.args):
    #     post_id = view_post_match.group(1)
    #     telegram_id = message.from_user.id
    #     status, post_details = await get_post_details(telegram_id, post_id)

    #     if not post_details or status != 200:
    #         await message.answer('Произошла ошибка при получении деталей поста.')
    #         return

    #     await send_post_user(
    #         message.bot,
    #         message.from_user.id,
    #         post_details
    #     )

    # if len(command.args.split(',')):
    #   message_ids = command.args.split(',')

    #    for message_id in message_ids:
    #        status, post_details = await get_post_details(message.from_user.id, message_id)
    #
    #        if status == 200:
    #            await send_post_user(
    #                message.bot,
    #                message.from_user.id,
    #                post_details
    #            )
    #        else:
    #            await message.answer(
    #                f'Не удалось получить детали для поста с ID: {message_id}'
    #            )

    # await message.answer(
    #     'Привет, это Postik! Нажмите кнопку ниже, чтобы отправить или посмотреть купленные посты.',
    #     reply_markup=MAIN_KB
    # )


# @dp.message(CommandStart())
# async def start_handler(message: types.Message):
#     await message.answer(
#         'Привет, это Postik! Нажмите кнопку ниже, чтобы отправить или посмотреть купленные посты.',
#         reply_markup=MAIN_KB
#     )


# @dp.message(F.text == 'Создать новый пост')
# async def process_post_message(message: types.Message, state: FSMContext):
#     await message.answer('Пожалуйста, отправьте ваше сообщение для поста.')
#     await state.set_state(PostStates.sending)


# # 2 handlers for creating posts
# @dp.message(PostStates.sending, F.media_group_id)
# async def post_media_group_handler(message: types.Message, state: FSMContext, album: list = None):
#     if message.has_protected_content:
#         await message.answer('Сообщение с защищенным контентом не может быть отправлено.')
#         return

#     message_info = await get_message_log_info(message)

#     message_id = await save_media_group_post(message, album)
#     if message_id is None:
#         await message.answer(SENDING_POST_ERR_MSG)
#         logger.error(
#             'Error saving message-post to MongoDB - %s.',
#             message_info
#         )
#         return

#     status, data = await send_post_to_api(
#         message.from_user.id,
#         message_id
#     )
#     if status == 201:
#         post_id = data['id']
#         await message.answer(f'Ваш пост под номером {post_id} был успешно сохранен.')
#     else:
#         logger.error(
#             'Error sending message-post to backend - %s',
#             message_info
#         )
#         await message.answer(SENDING_POST_ERR_MSG)

#     await state.clear()


# @dp.message(PostStates.sending)
# async def post_message_handler(message: types.Message, state: FSMContext):
#     if message.has_protected_content:
#         await message.answer('Сообщение с защищенным контентом не может быть отправлено.')
#         return

#     message_info = await get_message_log_info(message)

#     message_id = await save_message_post(message)
#     if message_id is None:
#         await message.answer(SENDING_POST_ERR_MSG)
#         logger.error(
#             'Error saving message-post to MongoDB - %s.',
#             message_info
#         )
#         return

#     status, data = await send_post_to_api(
#         message.from_user.id,
#         message_id
#     )
#     if status == 201:
#         post_id = data['id']
#         await message.answer(f'Ваш пост под названием "Пост №{post_id}" был успешно сохранен.')
#     else:
#         logger.error(
#             'Error sending message-post to backend - %s',
#             message_info
#         )
#         await message.answer(SENDING_POST_ERR_MSG)

#     await state.clear()


# @dp.message(F.text == 'Посмотреть посты')
# async def view_posts_handler(message: types.Message, state: FSMContext):
#     telegram_id = message.from_user.id
#     status, purchased_posts = await get_purchased_posts(telegram_id)

#     if not purchased_posts or status != 200:
#         await message.answer('У вас нет купленных постов.')
#         return

#     kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text=post['title'], callback_data=f"view_post_{post['id']}")]
#         for post in purchased_posts
#     ])

#     await message.answer('Ваши купленные посты:', reply_markup=kb)


# @dp.callback_query(lambda callback_query: callback_query.data.startswith('view_post_'))
# async def view_post_details_handler(callback_query: types.CallbackQuery):
#     telegram_id = callback_query.from_user.id
#     post_id = int(callback_query.data.split('_')[2])
#     status, post_details = await get_post_details(telegram_id, post_id)

#     if not post_details or status != 200:
#         await callback_query.message.answer('Произошла ошибка при получении деталей поста.')
#         return

#     await send_post_user(
#         callback_query.bot,
#         callback_query.from_user.id,
#         post_details
#     )


async def start_bot() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
