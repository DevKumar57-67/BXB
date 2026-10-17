from django.db import models

# Create your models here.

from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".m4v"}


def validate_vibe_media(file):
    extension = Path(file.name).suffix.lower()

    if extension not in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
        raise ValidationError(
            "Upload an image, GIF, or supported video file."
        )

    is_video = extension in VIDEO_EXTENSIONS
    max_size = 50 * 1024 * 1024 if is_video else 10 * 1024 * 1024

    if file.size > max_size:
        raise ValidationError(
            "Images and GIFs must be at most 10 MB. "
            "Videos must be at most 50 MB."
        )


class Vibe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vibes",
    )

    media = models.FileField(
        upload_to="vibes/%Y/%m/",
        validators=[validate_vibe_media],
    )

    caption = models.CharField(
        max_length=500,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_video(self):
        return Path(self.media.name).suffix.lower() in VIDEO_EXTENSIONS

    def __str__(self):
        return f"Vibe by {self.author.username} (#{self.pk})"
