from django.db import models
from cloudinary.models import CloudinaryField
from django.forms import ValidationError
from django.utils import timezone
from projects.models import Project
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='todo',
        help_text="Task status."
    )
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="Task priority level."
    )
    due_date = models.DateField(blank=True, null=True)
    assigned_to = models.ManyToManyField(
        'users.CustomUser',
        related_name='assigned_tasks',
        blank=True
    )
    created_by = models.ForeignKey('users.CustomUser', related_name='created_tasks', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    attachments = CloudinaryField('attachment', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError({'due_date': 'Due date cannot be in the past.'})

