
from django.urls import path

from .views import (
    clear_search_history,
    delete_search_history_item,
    search,
    search_suggestions,
)


urlpatterns = [
    path("", search, name="search"),

    path(
        "suggestions/",
        search_suggestions,
        name="search_suggestions",
    ),

    path(
        "history/clear/",
        clear_search_history,
        name="clear_search_history",
    ),

    path(
        "history/delete/",
        delete_search_history_item,
        name="delete_search_history_item",
    ),
]
