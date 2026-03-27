from django.contrib import admin
from .models import Task, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Detailed Admin view for Tasks.
    Enables quick tracking of status, priority, and assigned users.
    """
    list_display = ('id', 'title', 'board', 'status', 'priority', 'assignee', 'due_date')
    
    # Filters in the sidebar for easy project management
    list_filter = ('status', 'priority', 'board')
    
    search_fields = ('title', 'description', 'assignee__email', 'creator__email')
    
    # Make the UI more interactive by allowing status changes directly in the list view
    list_editable = ('status', 'priority')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Task Comments.
    """
    list_display = ('id', 'author', 'task', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__email', 'task__title')
    
    # Comments should usually be read-only in some fields for historical integrity
    readonly_fields = ('created_at',)