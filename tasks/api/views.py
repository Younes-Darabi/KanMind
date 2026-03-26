from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from rest_framework import serializers
from boards.models import Board
from tasks.api.permissions import IsBoardMember, IsCommentAuthor, IsTaskDeletePermission
from tasks.api.serializers import CommentSerializer, TaskSerializer
from tasks.models import Comment, Task


class TasksView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        board_id = request.data.get('board')
        board = get_object_or_404(Board, id=board_id)
        user = request.user
        if not (board.owner == user or board.members.filter(id=user.id).exists()):
            raise PermissionDenied(
                "Access denied. Board membership required.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, board)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, board):
        serializer.save(creator=self.request.user, board=board)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBoardMember(), IsTaskDeletePermission()]
        return [IsAuthenticated(), IsBoardMember()]

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class TaskAssignedToMeListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class TaskReviewingListView(generics.ListAPIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)

        if not (task.board.owner == self.request.user or task.board.members.filter(id=self.request.user.id).exists()):
            raise PermissionDenied(
                "Access denied. Board membership required.")
        return Comment.objects.filter(task=task).order_by('created_at')

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        user = self.request.user
        if not (task.board.owner == user or task.board.members.filter(id=user.id).exists()):
            raise PermissionDenied(
                "Access denied. Board membership required.")
        if not self.request.data.get('content'):
            raise serializers.ValidationError(
                {"content": "Content cannot be empty."})
        serializer.save(author=self.request.user, task=task)


class CommentDetailView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMember, IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_object(self):
        task_id = self.kwargs.get('task_id')
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, task_id=task_id)
        self.check_object_permissions(self.request, comment)
        return comment