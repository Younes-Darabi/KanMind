from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from boards.models import Board
from .permissions import IsBoardMemberOrOwner, IsOnlyOwner
from .serializers import BoardSerializer, SingleBoardSerializer, BoardPatchSerializer


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


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH']:
            return BoardPatchSerializer
        return SingleBoardSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsOnlyOwner()]
        return [IsAuthenticated(), IsBoardMemberOrOwner()]