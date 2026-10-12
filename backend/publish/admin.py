from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "creator",
        "category",
        "status",
        "views_count",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "creator__username",
        "technologies",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "published_at",
        "views_count",
    )

    ordering = ("-created_at",)

    list_per_page = 20
