from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models


class Project(models.Model):

    # --------------------------------------------------
    # PROJECT CATEGORIES
    # --------------------------------------------------

    class Category(models.TextChoices):
        AI_SOFTWARE = "ai_software", "AI & Software"
        WEB_APPS = "web_apps", "Web & Apps"
        UI_UX_DESIGN = "ui_ux_design", "UI/UX & Design"
        VIDEO_MOTION = "video_motion", "Video & Motion"
        PHOTO_EDITING = "photo_editing", "Photography & Editing"
        HARDWARE_ROBOTICS = "hardware_robotics", "Hardware & Robotics"
        OTHER = "other", "Other"

    # --------------------------------------------------
    # PUBLICATION STATUS
    # --------------------------------------------------

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    # --------------------------------------------------
    # CREATOR
    # --------------------------------------------------

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="studio_projects",
    )

    # --------------------------------------------------
    # BASIC PROJECT DETAILS
    # --------------------------------------------------

    title = models.CharField(max_length=120)

    description = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.OTHER,
    )

    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated technologies, frameworks, and tools.",
    )

    # --------------------------------------------------
    # PROJECT MEDIA
    # --------------------------------------------------

    cover_image = models.ImageField(
        upload_to="studio/covers/",
        blank=True,
        null=True,
    )

    demo_video_url = models.URLField(
        blank=True,
        max_length=500,
    )

    project_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Optional link to the live project or product.",
    )

    repository_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Optional link to the source-code repository.",
    )

    # --------------------------------------------------
    # STATUS AND ENGAGEMENT
    # --------------------------------------------------

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    published_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    # --------------------------------------------------
    # MODEL CONFIGURATION
    # --------------------------------------------------

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Studio Project"
        verbose_name_plural = "Studio Projects"

    def __str__(self):
        return self.title
