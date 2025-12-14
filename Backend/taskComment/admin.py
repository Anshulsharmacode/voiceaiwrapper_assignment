from django.contrib import admin
from .models import TaskComment


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('author_email', 'task', 'content_preview', 'timestamp')
    list_filter = ('timestamp', 'task')
    search_fields = ('author_email', 'content', 'task__title')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    def content_preview(self, obj):
        """Return a preview of the comment content."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
