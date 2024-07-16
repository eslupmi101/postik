from django.urls import path

from . import views

app_name = 'dashboards'


urlpatterns = [
    path('design/', views.DesignPageView.as_view(), name='design'),
    path('design/update-card/', views.update_card, name='update_card'),
    path('design/view-post/<int:post_id>/', views.view_post, name='view_post'),
    path('design/view-post-body/<int:post_id>/', views.view_post_body, name='view_post_body'),
    path('design/view-post-heading/<int:post_id>/', views.view_post_heading, name='view_post_heading'),
    path('design/view-posts-list/', views.view_posts_list, name='view_posts_list'),
    path('design/edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('design/preview-card/', views.preview_card, name='preview_card'),
]
