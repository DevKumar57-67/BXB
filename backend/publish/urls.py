
from django.urls import path
from . import views

app_name = "publish"

urlpatterns = [
    path("", views.create_project, name="create"),
]
