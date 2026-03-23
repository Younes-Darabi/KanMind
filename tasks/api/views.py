from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tasks.api.serializers import CommentSerializer, TaskSerializer
from tasks.models import Task, Comment
from .permissions import IsBoardMember, IsCommentAuthor


class TasksView(generics.ListCreateAPIView):
    """
    Handles listing and creating tasks.
    - LIST: Only returns tasks from boards where the user is an owner or member.
    - CREATE: Automatically sets the logged-in user as the 'creator'.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(board__owner=user) | Q(board__members=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific task.
    Access is restricted by IsBoardMember permission.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):

        user = self.request.user
        return Task.objects.filter(
            Q(board__owner=user) | Q(board__members=user)
        ).distinct()

    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)


class TaskAssignedToMeListView(generics.ListAPIView):
    """Returns a list of tasks where the current user is the Assignee."""
    
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class TaskReviewingListView(generics.ListAPIView):
    """Returns a list of tasks where the current user is the Reviewer."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class CommentListCreateView(generics.ListCreateAPIView):
    """
    Handles listing comments for a specific task and creating new ones.
    - LIST: Ordered by creation date (oldest first).
    - CREATE: Automatically links the comment to the task and the current user.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')

        return Comment.objects.filter(task_id=task_id).order_by('created_at')

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        
        serializer.save(author=self.request.user, task=task)


class CommentDetailView(generics.DestroyAPIView):
    """
    Handles deleting a comment.
    Ensures the comment belongs to the specified task and the user has permission.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated, IsBoardMember, IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_object(self):

        task_id = self.kwargs.get('task_id')
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, id=comment_id, task_id=task_id)