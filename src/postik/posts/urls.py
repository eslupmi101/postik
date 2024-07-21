from django.urls import path

from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('cards/<slug:telegram_username>/', views.card, name='card'),
]
