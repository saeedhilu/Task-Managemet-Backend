from django.db import models
from cloudinary.models import CloudinaryField
from django.forms import ValidationError
from django.utils import timezone
from projects.models import Project
from django.db import models
from core.utils.email import send_email
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.timezone import now
from users.models import Notification


class Tag(models.Model):
    """
    A model for tags used in tasks.
    
    """
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    A model for tasks.
    
    """
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
    ]
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="todo", help_text="Task status."
    )
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        default="medium",
        help_text="Task priority level.",
    )
    due_date = models.DateField(blank=True, null=True)
    assigned_to = models.ManyToManyField(
        "users.CustomUser", related_name="assigned_tasks", blank=True
    )
    created_by = models.ForeignKey(
        "users.CustomUser", related_name="created_tasks", on_delete=models.CASCADE
    )
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    attachments = CloudinaryField("attachment", blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError({"due_date": "Due date cannot be in the past."})

    def notify_assigned_members(self):
        """
        Notify the assigned members via email and send a notification to the group.
        
        
        """

        subject = f"New Task Assigned: {self.title}"
        message = f"""
        Hello,

        You have been assigned to a new task:
        Title: {self.title}
        Description: {self.description}
        Priority: {self.priority}
        Due Date: {self.due_date}

        Please check your task management system for more details.
        """
        recipients = [user.email for user in self.assigned_to.all()]
        send_email(subject, message, recipients)

        channel_layer = get_channel_layer()
        notification = {
            "type": "task_notification",
            "message": f"You have been assigned to a new task: {self.title}",
            "task_id": self.id,
        }
        
        for user in self.assigned_to.all():
            Notification.objects.create(
                recipient=user,
                actor=self.created_by,
                verb="assigned you to a task",
                description=f"Task: {self.title}\nPriority: {self.priority}",
                link=f"/tasks/{self.id}/",
                created_at=now(),
            )
            async_to_sync(channel_layer.group_send)(f"user_{user.id}", notification)
