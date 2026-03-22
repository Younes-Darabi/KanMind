from rest_framework import generics
from tasks.api.serializers import CommentSerializer, TaskSerializer
from tasks.models import Task, Comment
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBoardMember, IsCommentAuthor
from django.db.models import Q
from django.shortcuts import get_object_or_404



class TasksView(generics.ListCreateAPIView):

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
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')

        return Comment.objects.filter(task_id=task_id).order_by('created_at')

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        
        serializer.save(author=self.request.user, task=task)

class CommentDetailView(generics.DestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated, IsBoardMember, IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_object(self):

        task_id = self.kwargs.get('task_id')
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, id=comment_id, task_id=task_id)