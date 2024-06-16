from django.contrib import admin

from .models import TelegramProfile


class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'username', 'image', 'bio')
    search_fields = ('user__username', 'telegram_id', 'username')
    list_filter = ('user',)
    readonly_fields = ('telegram_id',)


admin.site.register(TelegramProfile, TelegramProfileAdmin)
