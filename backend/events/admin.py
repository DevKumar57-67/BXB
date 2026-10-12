from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    Event,
    EventRegistration,
    EventTeam,
    EventTeamMembership,
)


class EventTeamMembershipInline(admin.TabularInline):
    model = EventTeamMembership
    extra = 0
    autocomplete_fields = ["user"]


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    autocomplete_fields = ["user"]
    readonly_fields = ["registered_at"]


class EventTeamInline(admin.TabularInline):
    model = EventTeam
    extra = 0
    autocomplete_fields = ["leader"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organizer",
        "start_date",
        "registration_deadline",
        "participation_type",
        "status",
    )

    list_filter = (
        "status",
        "participation_type",
        "start_date",
    )

    search_fields = (
        "title",
        "organizer",
        "description",
        "venue",
    )

    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ("created_at", "updated_at")

    inlines = [
        EventRegistrationInline,
        EventTeamInline,
    ]

    fieldsets = (
        (
            "Event Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "organizer",
                    "venue",
                    "image",
                )
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "registration_deadline",
                )
            },
        ),
        (
            "Participation",
            {
                "fields": (
                    "participation_type",
                    "max_participants",
                    "min_team_size",
                    "max_team_size",
                    "registration_link",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "status",
                    "created_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "user",
        "registration_type",
        "status",
        "registered_at",
    )

    list_filter = (
        "status",
        "registration_type",
        "event",
    )

    search_fields = (
        "event__title",
        "user__email",
    )

    readonly_fields = ("registered_at",)


@admin.register(EventTeam)
class EventTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "event", "leader", "created_at")
    list_filter = ("event",)
    search_fields = ("name", "event__title", "leader__email")
    inlines = [EventTeamMembershipInline]
    readonly_fields = ("created_at",)