from django.contrib import admin
from .models import Task, Tag

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'status', 'priority', 'due_date', 'created_by', 'project', 'created_at']
    list_filter = ['status', 'priority', 'due_date', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    filter_horizontal = ['assigned_to']  # Use for many-to-many relations like assigned_to
    readonly_fields = ['created_at', 'updated_at']  # Make created_at and updated_at fields read-only

    # Optionally, customize the form fields
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'status', 'priority', 'due_date', 'assigned_to', 'project', 'attachments')  # Removed 'assigned_to' from here
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.id:  # If creating a new object
            obj.created_by = request.user  # Automatically set the created_by user
        super().save_model(request, obj, form, change)

admin.site.register(Task, TaskAdmin)
admin.site.register(Tag)  # Register the Tag model if you still need to use tags
