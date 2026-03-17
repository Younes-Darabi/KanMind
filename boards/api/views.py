from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from boards.api.permissions import IsOwnerOrReadOnly
from boards.models import Board
from .serializers import BoardSerializer


class BoardsView(generics.ListCreateAPIView):

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SingleBoardView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]