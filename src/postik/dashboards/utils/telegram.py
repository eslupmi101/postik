from django.conf import settings


def get_telegram_create_post_link() -> str:
    return f'tg://resolve?domain={settings.BOT_HANDLER_NAME}&start=create_post'
