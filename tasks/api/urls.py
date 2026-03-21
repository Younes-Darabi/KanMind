from django.urls import path
from .views import TasksView, TaskDetailView, TaskReviewingListView, TaskAssignedToMeListView


urlpatterns = [
    path('', TasksView.as_view(), name='tasks_list_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('reviewing/', TaskReviewingListView.as_view(), name='tasks_reviewing_list'),
    path('assigned-to-me/', TaskAssignedToMeListView.as_view(), name='tasks-assigned-to-me'),
]
