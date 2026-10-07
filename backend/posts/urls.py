from django.urls import path

from .views import feed, delete_post


urlpatterns = [
    path('', feed, name='feed'),
    path(
        'delete/<int:post_id>/',
        delete_post,
        name='delete_post'
    ),
]