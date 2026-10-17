
from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    bio = models.TextField(max_length=500, blank=True)
    college = models.CharField(max_length=150, blank=True)
    course = models.CharField(max_length=100, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True)
    interests = models.CharField(max_length=500, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_user_follow",
            ),
            models.CheckConstraint(
                condition=~models.Q(
                    follower=models.F("following")
                ),
                name="prevent_self_follow",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.follower.username} follows "
            f"{self.following.username}"
        )
