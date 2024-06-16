from django.urls import path

from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('cards/<int:card_id>/', views.card, name='card'),
    path('post-cart/<int:card_id>/<int:post_id>/', views.post_card, name='post_cart'),
]
