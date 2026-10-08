from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Handshake(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"


    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="handshakes_sent"
    )


    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="handshakes_received"
    )


    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=["sender", "receiver"],
                name="unique_handshake_request"
            )

        ]

        ordering = ["-created_at"]


    def __str__(self):

        return (
            f"{self.sender.username} → "
            f"{self.receiver.username} "
            f"({self.status})"
        )