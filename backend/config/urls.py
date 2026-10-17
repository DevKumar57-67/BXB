"""URL configuration for the project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("auth/", include("users.urls")),
    path("profile/", include("profiles.urls")),
    path("feed/", include("posts.urls")),
    path("search/", include("search.urls")),
    path("handshake/", include("handshake.urls")),
    path("notifications/", include("notifications.urls")),
    path("ai-studio/", include("ai_studio.urls")),
    path("events/", include("events.urls")),
    path("publish/", include("publish.urls")),
    path(
        "vibespace/",
        include("vibespace.urls"),
    ),
    

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)