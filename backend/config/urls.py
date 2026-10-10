"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('users.urls')),
]


from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('users.urls')),
]



from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('users.urls')),
    path('profile/', include('profiles.urls'

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),

    path('auth/', include('users.urls')),

    path('profile/', include('profiles.urls')),

    path('feed/', include('posts.urls')),
]



from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),

    path('auth/', include('users.urls')),

    path('profile/', include('profiles.urls')),

    path('feed/', include('posts.urls')),

     path('search/', include('search.urls')),

     path('handshake/', include('handshake.urls')),

     path('notifications/', include('notifications.urls')),

     path("ai-studio/", include("ai_studio.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    """


from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    # Main website
    path("", include("core.urls")),

    # Authentication
    path("auth/", include("users.urls")),

    # User profiles
    path("profile/", include("profiles.urls")),

    # Feed and social interactions
    path("feed/", include("posts.urls")),

    # Search
    path("search/", include("search.urls")),

    # Handshake connections
    path("handshake/", include("handshake.urls")),

    # Notifications
    path("notifications/", include("notifications.urls")),

    # AI Studio dashboard
    path("ai-studio/", include("ai_studio.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )