from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users.models import  Notification
from .models import  Task

from django.utils.timezone import now

@receiver(post_save, sender=Task)
def send_task_update_notification(sender, instance, created, **kwargs):
    print("Sending task update notification")
        # -----------
        # it will trigger a notification when a task is updated
        #------------
    if not created:  
        print("Task update notification0")
        channel_layer = get_channel_layer()
        message = f"The task '{instance.title}' has been updated."
        
        
        for user in instance.assigned_to.all():
            Notification.objects.create(
                recipient=user,             
                actor=instance.created_by,     
                verb='task_updated',
                description=message,
                link=f"/tasks/{instance.id}/",
                created_at=now()
            )
            
            group_name = f"user_{user.id}"
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "task_notification",
                    "message": message,
                    "task_id": instance.id,
                }
            )
