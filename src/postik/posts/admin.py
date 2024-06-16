from django.contrib import admin

from .models import Post, Card, CardPost


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'description', 'price', 'image')
    search_fields = ('id', 'title', 'user__username', 'description')
    list_filter = ('user',)


class CardPostInline(admin.TabularInline):
    model = CardPost
    extra = 1


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'is_active')
    search_fields = ('id', 'title', 'user__username', 'description')
    list_filter = ('user', 'is_active')
    filter_horizontal = ('posts',)
    inlines = [CardPostInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Card, CardAdmin)
