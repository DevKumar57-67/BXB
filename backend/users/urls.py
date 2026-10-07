"""

from django.urls import path

from .views import register, login_view, logout_view


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

"""

from django.urls import path

from .views import (
    register,
    login_view,
    logout_view,
    verify_otp,
)


urlpatterns = [
    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'verify-otp/',
        verify_otp,
        name='verify_otp'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),
]