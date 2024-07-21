from django.urls import path

from . import views

app_name = 'dashboards'


urlpatterns = [
    path('design/', views.DesignPageView.as_view(), name='design'),
    path('design/update-card/', views.update_card, name='update_card'),

    path('design/publish-card/', views.publish_card, name='publish_card'),
    path('design/unpublish-card/', views.unpublish_card, name='unpublish_card'),

    path('design/view-post-body/<int:post_id>/', views.view_post_body, name='view_post_body'),
    path('design/view-post-heading/<int:post_id>/', views.view_post_heading, name='view_post_heading'),
    path('design/view-posts-list/', views.view_posts_list, name='view_posts_list'),
    path('design/delete-post-card/<int:post_id>/', views.delete_post_card, name='delete_post_card'),
    path('design/add-post-card/<int:post_id>/', views.add_post_card, name='add_post_card'),

    path('design/view-post/<int:post_id>/', views.view_post, name='view_post'),
    path('design/create-post/', views.create_post, name='create_post'),
    path('design/edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('design/remove-post/<int:post_id>/', views.remove_post, name='remove_post'),

    path('design/preview-card/', views.preview_card, name='preview_card'),
]
