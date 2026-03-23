from django.db import models

from boards.models import Board
from users.models import User


class Task(models.Model):
    """
    Represents a task within a specific Board.
    Includes workflow status, priority levels, and assignment logic.
    """

    class Status(models.TextChoices):
        TODO = 'to-do', 'To Do'
        IN_PROGRESS = 'in-progress', 'In Progress'
        REVIEW = 'review', 'Review'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    # Relationships
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='tasks')
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_tasks'
    )
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_tasks')
    
    # Task Details
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TODO)
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField()


    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a discussion comment on a specific Task.
    """

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.fullname} on {self.task.title}"