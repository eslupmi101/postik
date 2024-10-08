from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(
    'posts',
    views.PostCreateViewSet,
    basename='posts'
)
router.register(
    'posts/purchase',
    views.PostPurchaseViewSet,
    basename='posts_purchase'
)
router.register(
    'leads',
    views.LeadViewSet,
    basename='leads'
)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/bot_manager/', views.BotManagerAuthView.as_view(), name='bot_manager'),
    path('auth/telegram/', views.AuthTelegramCheckView.as_view(), name='auth_telegram_check'),
]
