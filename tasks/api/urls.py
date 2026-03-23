from django.urls import path
from .views import (
    CommentDetailView,
    CommentListCreateView,
    TasksView,
    TaskDetailView,
    TaskReviewingListView,
    TaskAssignedToMeListView
)

# URL Configuration for Tasks and Comments.
# These endpoints manage the core workflow of the KanMind application.

urlpatterns = [
    # --- Task Management ---
    # GET: List all tasks user has access to | POST: Create a new task
    path('', TasksView.as_view(), name='tasks_list_create'),

    # GET: Retrieve | PUT/PATCH: Update | DELETE: Remove a specific task
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),

    # --- Specialized Task Filters ---
    # GET: List tasks where the current user is the Reviewer
    path('reviewing/', TaskReviewingListView.as_view(),
         name='tasks_reviewing_list'),

    # GET: List tasks where the current user is the Assignee
    path('assigned-to-me/', TaskAssignedToMeListView.as_view(),
         name='tasks_assigned_to_me'),

    # --- Comment System (Nested) ---
    # GET: List all comments for a task | POST: Add a comment to a task
    path('<int:task_id>/comments/', CommentListCreateView.as_view(),
         name='comment_list_create'),

    # DELETE: Remove a specific comment from a specific task
    path('<int:task_id>/comments/<int:comment_id>/',
         CommentDetailView.as_view(), name='comment_delete'),
]
