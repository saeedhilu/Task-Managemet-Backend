from .models import Mention, Notification, CustomUser
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from channels.layers import get_channel_layer
from django.utils.timezone import now
from asgiref.sync import async_to_sync


@receiver(m2m_changed, sender=Mention.mentioned_user.through)
def send_mention_notification(sender, instance, action, pk_set, **kwargs):
    """
    Signal to handle notifications when users are mentioned in a task.
    """
    if action == "post_add":

        mentioned_users = CustomUser.objects.filter(pk__in=pk_set)
        if not mentioned_users.exists():
            # dont want to send notifications
            return

        channel_layer = get_channel_layer()
        for user in mentioned_users:

            description = f'{instance.mentioned_by.username} mentioned you in task "{instance.task.title}".'

            Notification.objects.create(
                recipient=user,
                actor=instance.mentioned_by,
                verb="mentioned_you",
                description=description,
                link=f"/tasks/{instance.task.id}/",
                created_at=now(),
            )

            group_name = f"user_{user.id}"
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "task_notification",
                    "message": description,
                    "task_id": instance.task.id,
                },
            )
