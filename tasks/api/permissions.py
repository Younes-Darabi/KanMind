from rest_framework import permissions
from boards.models import Board

class IsBoardMember(permissions.BasePermission):

    def has_permission(self, request, view):

        board_id = view.kwargs.get('pk') 

        try:
            board = Board.objects.get(pk=board_id)
            return board.owner == request.user or board.members.filter(id=request.user.id).exists()
        
        except Board.DoesNotExist:
            return False
        
    