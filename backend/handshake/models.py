'''

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

    # Short explanation of the collaboration idea.
    description = models.CharField(
        max_length=500,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
'''


from django.conf import settings
from django.db import models


class Handshake(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    class Stage(models.TextChoices):
        IDEA = "idea", "Idea"
        PROTOTYPE = "prototype", "Prototype"
        PRODUCT = "product", "Working Product"

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="handshakes_sent",
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="handshakes_received",
    )

    # Collaboration proposal details
    title = models.CharField(
        max_length=120,
        blank=True,
        default="",
    )

    description = models.CharField(
        max_length=500,
        blank=True,
    )

    stage = models.CharField(
        max_length=20,
        choices=Stage.choices,
        default=Stage.IDEA,
    )

    demo_video_url = models.URLField(
        blank=True,
    )

    collaboration_needs = models.CharField(
        max_length=500,
        blank=True,
    )

    # Request status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                name="unique_handshake_request",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.sender.username} → "
            f"{self.receiver.username} ({self.status})"
        )


class HandshakeImage(models.Model):
    handshake = models.ForeignKey(
        Handshake,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="handshake_images/",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["uploaded_at"]

    def __str__(self):
        return f"Image for handshake #{self.handshake_id}"
