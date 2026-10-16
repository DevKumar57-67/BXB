from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models


class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_history",
    )

    query = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Search History"
        verbose_name_plural = "Search Histories"

    def __str__(self):
        return f"{self.user} searched for '{self.query}'"
