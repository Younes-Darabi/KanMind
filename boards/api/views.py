from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from boards.models import Board
from .permissions import IsOnlyOwner
from .serializers import BoardSerializer, SingleBoardSerializer


class BoardsView(generics.ListCreateAPIView):
    """
    API view to list and create Boards.
    - LIST: Returns boards where the user is either the owner or a member.
    - CREATE: Sets the current user as the owner and adds them to the members list.
    """

    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters boards to ensure users only see projects they are involved in.
        Uses .distinct() to prevent duplicate results from M2M relationships.
        """

        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Automatically assigns the logged-in user as the board owner 
        and adds them to the members group upon creation.
        """

        board = serializer.save(owner=self.request.user)
        board.members.add(self.request.user)


class SingleBoardView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific board.
    Access is restricted to board owners and members, 
    but only the owner can delete the board.
    """

    serializer_class = SingleBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensures the user can only interact with boards they have access to.
        """

        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()
    
    def get_permissions(self):
        """
        Dynamically applies permissions based on the HTTP method.
        - DELETE: Requires the user to be both authenticated and the owner.
        - OTHER: Requires only authentication (access controlled by queryset).
        """

        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsOnlyOwner()]
        return [IsAuthenticated()]