from django.urls import path

from .views import edit_profile, my_profile, public_profile

urlpatterns = [
    path("", my_profile, name="my_profile"),
    path("edit/", edit_profile, name="edit_profile"),
    path("u/<str:username>/", public_profile, name="public_profile"),
]
