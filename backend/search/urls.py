from django.urls import path

from .views import search, search_suggestions


urlpatterns = [
    path("", search, name="search"),
    path(
        "suggestions/",
        search_suggestions,
        name="search_suggestions"
    ),
]