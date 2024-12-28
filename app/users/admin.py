from django.contrib import admin
from .models import CustomUser, Comment, Mention, Notification


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "is_staff",
        "role",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("email", "username")
    list_filter = ("is_staff", "is_active", "role")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "created_by", "text", "created_at")
    search_fields = ("task__title", "created_by__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "mentioned_by", "created_at")
    search_fields = ("task__title", "mentioned_by__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "actor", "verb", "description", "created_at")
    search_fields = ("recipient__username", "actor__username", "verb", "description")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
