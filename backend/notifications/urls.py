from django.urls import path

from .views import (
    notification_list,
    unread_count,
    mark_as_read,
    mark_all_as_read,
)


urlpatterns = [

    path(
        "",
        notification_list,
        name="notification_list"
    ),

    path(
        "unread-count/",
        unread_count,
        name="unread_count"
    ),

    path(
        "read/<int:notification_id>/",
        mark_as_read,
        name="mark_as_read"
    ),

    path(
        "read-all/",
        mark_all_as_read,
        name="mark_all_as_read"
    ),

]