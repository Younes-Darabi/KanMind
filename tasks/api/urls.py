from django.urls import path
from .views import TasksView, SingleTaskView


urlpatterns = [
    path('', TasksView.as_view(), name='tasks_view'),
    path('<int:pk>/', SingleTaskView.as_view(), name='single_task_view'),
]
