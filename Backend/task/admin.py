from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'assignee_email', 'due_date', 'created_at')
    list_filter = ('status', 'created_at', 'project', 'due_date')
    search_fields = ('title', 'description', 'assignee_email', 'project__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'due_date'
