from django.urls import path

from . import views

app_name = 'dashboards'


urlpatterns = [
    path('design/', views.design, name='design'),
    path('design/update_card/', views.update_card, name='update_card'),
    path('design/modal-posts/', views.modal_posts, name='modal-posts'),
    path('design/update-post/<int:post_id>/', views.update_post, name='update_post'),
    path('design/save-card/', views.save_card, name='save_card'),

    path('design/card-posts', views.card_posts, name='card-posts'),
    path('design/preview_card', views.preview_card, name='preview_card'),

    path('connect/', views.connect, name='connect'),
]
