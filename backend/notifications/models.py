from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):

        LIKE = "like", "Like"
        COMMENT = "comment", "Comment"
        REPOST = "repost", "Repost"

        HANDSHAKE_RECEIVED = (
            "handshake_received",
            "Handshake Received"
        )

        HANDSHAKE_ACCEPTED = (
            "handshake_accepted",
            "Handshake Accepted"
        )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_created"
    )

    notification_type = models.CharField(
        max_length=40,
        choices=NotificationType.choices
    )

    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    handshake = models.ForeignKey(
        "handshake.Handshake",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    comment = models.ForeignKey(
        "posts.Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    message = models.CharField(
        max_length=255,
        blank=True
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):

        return (
            f"{self.actor.username} → "
            f"{self.recipient.username}: "
            f"{self.notification_type}"
        )