from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


class Event(models.Model):
    class ParticipationType(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        TEAM = "team", "Team"
        BOTH = "both", "Individual or Team"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    organizer = models.CharField(max_length=150)
    venue = models.CharField(max_length=200, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()

    participation_type = models.CharField(
        max_length=10,
        choices=ParticipationType.choices,
        default=ParticipationType.BOTH,
    )

    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank for unlimited individual registrations.",
    )

    min_team_size = models.PositiveIntegerField(default=2)
    max_team_size = models.PositiveIntegerField(default=4)

    image = models.URLField(
        blank=True,
        help_text="Optional public image URL for the event banner.",
    )

    registration_link = models.URLField(
        blank=True,
        help_text="Optional external registration link.",
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_events",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_date", "title"]

    def __str__(self):
        return self.title

    @property
    def is_registration_open(self):
        now = timezone.now()

        return (
            self.status == self.Status.PUBLISHED
            and now < self.registration_deadline
            and now < self.start_date
        )

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()


class EventRegistration(models.Model):
    class RegistrationType(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        TEAM = "team", "Team"

    class Status(models.TextChoices):
        REGISTERED = "registered", "Registered"
        CANCELLED = "cancelled", "Cancelled"

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )

    registration_type = models.CharField(
        max_length=10,
        choices=RegistrationType.choices,
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.REGISTERED,
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-registered_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["event", "user"],
                name="unique_event_registration_per_user",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.event.title}"


class EventTeam(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="teams",
    )

    name = models.CharField(max_length=100)

    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="led_event_teams",
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="EventTeamMembership",
        related_name="event_teams",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "name"],
                name="unique_team_name_per_event",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.event.title}"


class EventTeamMembership(models.Model):
    team = models.ForeignKey(
        EventTeam,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_team_memberships",
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "user"],
                name="unique_user_per_event_team",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.team.name}"