from aiogram import Bot


async def send_post_message(bot: Bot, user_id: str, post_details: dict[str]):
    await bot.forward_message(
        chat_id=user_id,
        from_chat_id=post_details['telegram_id'],
        message_id=post_details['message_id']
    )

    description = post_details.get('description', 'Описание отсутствует')
    price = post_details.get('price', 'Цена отсутствует')

    await bot.send_message(
        user_id,
        f"Название: {post_details['title']}\nОписание: {description}\nЦена: {price}"
    )
