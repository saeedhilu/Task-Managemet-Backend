from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Project(models.Model):
    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("on_hold", "On Hold"),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    members = models.ManyToManyField("users.CustomUser", related_name="projects")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_started",
        help_text="Current status of the project.",
    )
    created_by = models.ForeignKey(
        "users.CustomUser", related_name="created_projects", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
