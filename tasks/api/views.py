from rest_framework import generics
from tasks.api.serializers import TaskSerializer
from tasks.models import Task
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBoardMember


class TasksView(generics.ListCreateAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def perform_create(self, serializer):
        
        board_id = self.kwargs.get('board_pk')
        serializer.save(board_id=board_id)

class SingleTaskView(generics.ListCreateAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]