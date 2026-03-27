from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from boards.models import Board
from .permissions import IsBoardMemberOrOwner, IsOnlyOwner
from .serializers import BoardSerializer, SingleBoardSerializer, BoardPatchSerializer


class BoardsView(generics.ListCreateAPIView):
    """
    Handles listing boards accessible to the user and creating new boards.
    """
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a list of boards where the current user is either 
         the owner OR a member.
        """
        user = self.request.user
        """Use Q objects for OR condition: (Owner == User) OR (Member contains User)"""
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct() 

    def perform_create(self, serializer):
        """
        Saves the new board and automatically adds the creator as 
        both the owner and a member.
        """
        board = serializer.save(owner=self.request.user)
        board.members.add(self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating (PATCH), and deleting a specific board.
    Dynamically switches serializers and permissions based on the request method.
    """
    queryset = Board.objects.all()

    def get_serializer_class(self):
        """
        Returns BoardPatchSerializer for partial updates (PATCH) 
        and SingleBoardSerializer for standard retrieval (GET).
        """
        if self.request.method in ['PATCH']:
            return BoardPatchSerializer
        return SingleBoardSerializer

    def get_permissions(self):
        """
        Strict permission logic:
        - DELETE: Restricted to the board owner only (IsOnlyOwner).
        - GET/PATCH: Accessible by both members and the owner (IsBoardMemberOrOwner).
        """
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsOnlyOwner()]
        return [IsAuthenticated(), IsBoardMemberOrOwner()]