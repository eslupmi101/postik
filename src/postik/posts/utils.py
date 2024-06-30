from django.conf import settings


def get_telegram_purchased_posts_link(posts_id: list[int]) -> str:
    posts_id = [str(id) for id in posts_id]
    posts_id_str = ','.join(posts_id)
    return f'https://t.me/{settings.BOT_HANDLER_NAME}?start={posts_id_str}'
