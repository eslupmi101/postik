from rest_framework.permissions import BasePermission
from django.conf import settings


class BotManagerTokenPermission(BasePermission):
    def has_permission(self, request, *_):
        return request.headers.get('Bot-Token') == settings.BOT_MANAGER_TOKEN


class BotHandlerTokenPermission(BasePermission):
    def has_permission(self, request, *_):
        return request.headers.get('Bot-Token') == settings.BOT_HANDLER_TOKEN


class AuthTelegramCheckPermission(BasePermission):
    def has_permission(self, request, *_):
        return not request.user.is_authenticated
