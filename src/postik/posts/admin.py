from django.contrib import admin

from .models import Card, CardPost, Post, PostPurchase, Lead


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


class PostPurchaseAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('post', 'user')
    search_fields = ('post__title', 'user__username')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post', 'user')


class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'subscriber_username', 'subscriber_telegram_id')
    list_filter = ('post', 'author')
    search_fields = ('subscriber_username', 'subscriber_telegram_id')
    ordering = ('-id',)
    readonly_fields = ('id',)

    def get_queryset(self, request):
        # Optionally limit the queryset based on the user or other logic
        queryset = super().get_queryset(request)
        return queryset

    def save_model(self, request, obj, form, change):
        # Optionally modify obj before saving
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(PostPurchase, PostPurchaseAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Lead, LeadAdmin)
