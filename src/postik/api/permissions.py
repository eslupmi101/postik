from rest_framework.permissions import BasePermission
from django.conf import settings

from users.models import BotAccessToken


class BotManagerTokenPermission(BasePermission):
    def has_permission(self, request, *_):
        return BotAccessToken.objects.filter(
            token=request.headers.get('Bot-Token'),
            bot_name=settings.BOT_MANAGER_NAME
        ).exists()


class BotHandlerTokenPermission(BasePermission):
    def has_permission(self, request, *_):
        return BotAccessToken.objects.filter(
            token=request.headers.get('Bot-Token'),
            bot_name=settings.BOT_HANDLER_NAME
        ).exists()


class AuthTelegramCheckPermission(BasePermission):
    def has_permission(self, request, *_):
        return not request.user.is_authenticated
