from django.contrib import admin

from .models import BotAccessToken, TelegramProfile


class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'username', 'image', 'bio')
    search_fields = ('user__username', 'telegram_id', 'username')
    list_filter = ('user',)


class BotAccessTokenAdmin(admin.ModelAdmin):
    list_display = ('bot_name', 'token')
    search_fields = ('bot_name',)


admin.site.register(BotAccessToken, BotAccessTokenAdmin)
admin.site.register(TelegramProfile, TelegramProfileAdmin)
