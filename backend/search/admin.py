from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "query", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "query")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
