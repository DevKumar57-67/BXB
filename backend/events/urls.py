from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("create/", views.create_event, name="create_event"),
    path("my-events/", views.my_events, name="my_events"),
    path("<slug:slug>/", views.event_detail, name="event_detail"),
    path("<slug:slug>/register/", views.register_event, name="register_event"),
    path("<slug:slug>/cancel-registration/", views.cancel_registration, name="cancel_registration"),
    path("<slug:slug>/create-team/", views.create_team, name="create_team"),
    path("<slug:slug>/join-team/<int:team_id>/", views.join_team, name="join_team"),
]
