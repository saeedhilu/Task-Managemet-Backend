# tasks/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task

# @receiver(post_save, sender=Task,)
# def notify_on_task_assignment(sender, instance,created, **kwargs):

    
#     print(created)

#     if created == True :  # Trigger after a task creation
#         print("sdjdhjsdhj")
        # instance.notify_assigned_members()
