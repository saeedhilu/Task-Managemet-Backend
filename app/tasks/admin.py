from django.contrib import admin
from .models import Task, Tag


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "status",
        "priority",
        "due_date",
        "created_by",
        "project",
        "created_at",
    ]
    list_filter = ["status", "priority", "due_date", "created_at"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
    filter_horizontal = [
        "assigned_to"
    ] 
    readonly_fields = [
        "created_at",
        "updated_at",
    ] 

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "status",
                    "priority",
                    "due_date",
                    "assigned_to",
                    "project",
                    "attachments",
                )  
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user 
        super().save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)
admin.site.register(Tag)
