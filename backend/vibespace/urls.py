
from django.urls import path

from . import views

app_name = "vibespace"

urlpatterns = [
    path(
        "create/",
        views.create_vibe,
        name="create",
    ),
    path(
        "explore/",
        views.explore_vibes,
        name="explore",
    ),
    path(
        "my/",
        views.my_vibes,
        name="my_vibes",
    ),
    path(
        "<int:pk>/",
        views.vibe_detail,
        name="detail",
    ),
]
