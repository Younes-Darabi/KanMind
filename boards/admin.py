from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Admin configuration for Board management.
    Shows ownership and allows filtering by board owners.
    """
    list_display = ('id', 'title', 'owner', 'get_members_count')
    search_fields = ('title', 'owner__email')
    list_filter = ('owner',)

    def get_members_count(self, obj):
        """Custom column to show the number of members in the list view."""
        return obj.members.count()
    
    """Sets the column header name in the Admin panel"""
    get_members_count.short_description = 'Members Count'