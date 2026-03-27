from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Configuration for the Custom User model in the Django Admin panel.
    Displays essential user info and provides search by email/fullname.
    """
    # Columns to display in the user list view
    list_display = ('id', 'email', 'fullname', 'is_staff', 'is_active')
    
    # Enable searching by these fields
    search_fields = ('email', 'fullname')
    
    # Sidebar filters to quickly find staff or active/inactive users
    list_filter = ('is_staff', 'is_active')
    
    # Ordering users by ID in descending order
    ordering = ('-id',)