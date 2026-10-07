from django.urls import path
from .views import *


urlpatterns = [
    path('', bxb, name='bxb'),
]