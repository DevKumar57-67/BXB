from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'college',
        'course',
        'year',
        'created_at',
    )

    search_fields = (
        'user__username',
        'college',
        'course',
        'skills',
        'interests',
    )