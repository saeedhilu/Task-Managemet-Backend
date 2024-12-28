from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# from cloudinary.models import CloudinaryField
from rest_framework_simplejwt.tokens import RefreshToken
from .manager import CustomUserManager
from django.core.validators import (
    EmailValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.contrib.auth.password_validation import validate_password

# from tasks.models import Task
from django.utils.timezone import now


class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("member", "Team Member"),
        ("project_manager", "Project Manager"),
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address")],
        max_length=255,
        help_text="Required. A valid email address.",
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            MinLengthValidator(5, message="Username must be at least 5 characters long")
        ],
        help_text="Required. At least 5 characters long.",
    )
    password = models.CharField(
        max_length=128,
        validators=[validate_password],
        help_text="Password must be at least 8 characters long, contain an uppercase letter, a number, and a special character.",
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # TODO: modification (1)
    # profile_picture = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"

    @property
    def tokens(self) -> dict[str, str]:
        referesh = RefreshToken.for_user(self)

        return {
            "refresh": str(referesh),
            "access": str(referesh.access_token),
        }


class Comment(models.Model):
    task = models.ForeignKey(
        "tasks.Task", on_delete=models.CASCADE, related_name="comments"
    )
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by} on {self.task.title}"


class Mention(models.Model):
    task = models.ForeignKey(
        "tasks.Task", on_delete=models.CASCADE, related_name="mentions"
    )
    mentioned_user = models.ManyToManyField(
        CustomUser, related_name="mentions_received"
    )
    mentioned_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="mentions_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="related_notifications"
    )
    verb = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
