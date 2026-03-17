from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from boards import models
from boards.api.permissions import IsOwnerOrReadOnly
from boards.models import Board
from .serializers import BoardSerializer


class BoardsView(generics.ListCreateAPIView):

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):

        board = serializer.save(owner=self.request.user)
        board.members.add(self.request.user)


class SingleBoardView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(models.Q(owner=user) | models.Q(members=user)).distinct()