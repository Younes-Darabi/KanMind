from django.urls import path
from .views import (
    CommentDetailView,
    CommentListCreateView,
    TasksView,
    TaskDetailView,
    TaskReviewingListView,
    TaskAssignedToMeListView
)

# Define URL patterns for Task and Comment management
urlpatterns = [
    # List tasks where the current user is set as the Reviewer
    path('reviewing/', TaskReviewingListView.as_view(), name='tasks_reviewing_list'),
    
    # List tasks assigned specifically to the authenticated user
    path('assigned-to-me/', TaskAssignedToMeListView.as_view(), name='tasks_assigned_to_me'),
    
    # Global task endpoints: GET to list all accessible tasks, POST to create a new one
    path('', TasksView.as_view(), name='tasks_list_create'),
    
    # Detail endpoint for a specific task: GET (retrieve), PATCH (update), DELETE (remove)
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    
    # Nested comments: List all comments for a specific task or POST a new comment
    path('<int:task_id>/comments/', CommentListCreateView.as_view(), name='comment_list_create'),
    
    # Specific comment endpoint: DELETE a comment belonging to a specific task
    path('<int:task_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment_delete'),
]