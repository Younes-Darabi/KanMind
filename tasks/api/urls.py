from django.urls import path
from .views import (
    CommentDetailView,
    CommentListCreateView,
    TasksView,
    TaskDetailView,
    TaskReviewingListView,
    TaskAssignedToMeListView
)


urlpatterns = [
    path('reviewing/', TaskReviewingListView.as_view(), name='tasks_reviewing_list'),
    path('assigned-to-me/', TaskAssignedToMeListView.as_view(), name='tasks_assigned_to_me'),
    path('', TasksView.as_view(), name='tasks_list_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:task_id>/comments/', CommentListCreateView.as_view(), name='comment_list_create'),
    path('<int:task_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment_delete'),
]