from django.urls import path

from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('cards/<slug:telegram_username>/', views.card, name='card'),
    path('post-cart/<int:card_id>/<int:post_id>/', views.post_card, name='post_cart'),
    path('buy_posts/<int:card_id>/', views.buy_posts, name='buy_posts')
]
