from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from boards.models import Board
from .serializers import BoardSerializer, SingleBoardSerializer
from django.db.models import Q
from .permissions import IsOnlyOwner

class BoardsView(generics.ListCreateAPIView):

    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        board.members.add(self.request.user)


class SingleBoardView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = SingleBoardSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()
    
    def get_permissions(self):

        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsOnlyOwner()]
        return [IsAuthenticated()]