from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Project


@receiver(post_save, sender=Project)
def invalidate_all_users_project_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate all users project cache on save operation on the given instance
    """
    cache_key_pattern = f"project_list_user_*"
    keys_to_delete = cache.keys(cache_key_pattern)
    for key in keys_to_delete:
        cache.delete(key)


@receiver(post_delete, sender=Project)
def invalidate_project_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the project cache on delete operation on the given instance
    """
    cache_key = f"project_list_user_{instance.created_by.id}"
    cache.delete(cache_key)
