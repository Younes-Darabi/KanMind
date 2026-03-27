from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.api.urls')),
    path('api/tasks/', include('tasks.api.urls')),
    path('api/boards/', include('boards.api.urls')),
]