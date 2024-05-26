from rest_framework.permissions import BasePermission
from django.conf import settings


class BotTokenPermission(BasePermission):
    def has_permission(self, request, *_):
        bot_token = request.headers.get('Bot-Token')
        return bot_token == settings.BOT_MANAGER_TOKEN


class AuthTelegramCheckPermission(BasePermission):
    def has_permission(self, request, *_):
        return not request.user.is_authenticated
