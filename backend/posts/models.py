from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    content = models.TextField(
        max_length=2000
    )

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"


class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_likes"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_post_like"
            )
        ]

        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"


class PostSave(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_posts"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="saves"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_post_save"
            )
        ]

        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} saved post {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField(
        max_length=1000
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} on post {self.post.id}"


class Repost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reposts"
    )

    original_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reposts"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "original_post"],
                name="unique_post_repost"
            )
        ]

        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} reposted "
            f"post {self.original_post.id}"
        )