from django.urls import path

from . import views

app_name = 'api'


urlpatterns = [
    path('auth/bot_manager/', views.BotManagerAuthView.as_view(), name='bot_manager'),
    path('auth/telegram/', views.AuthTelegramCheckView.as_view(), name='auth_telegram_check'),
]
