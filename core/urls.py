from django.contrib import admin
from django.urls import include, path

# The main URL configuration for the entire project.
# It routes requests to the appropriate app-specific URL files.
urlpatterns = [
    # Django Administration panel: /admin/
    path('admin/', admin.site.urls),
    
    # User-related endpoints: /api/registration/, /api/login/, etc.
    path('api/', include('users.api.urls')),
    
    # Task and Comment management: /api/tasks/
    path('api/tasks/', include('tasks.api.urls')),
    
    # Project Board management: /api/boards/
    path('api/boards/', include('boards.api.urls')),
]