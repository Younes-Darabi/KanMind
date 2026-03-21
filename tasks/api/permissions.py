from rest_framework import permissions
from boards.models import Board

class IsBoardMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user
        
        if request.method == 'DELETE':
            return obj.creator == user or obj.board.owner == user
        
        return obj.board.owner == user or obj.board.members.filter(id=user.id).exists()

    def has_permission(self, request, view):

        if request.method == 'POST':
            board_id = request.data.get('board')
            if not board_id:
                return False
            try:
                board = Board.objects.get(pk=board_id)
                return board.owner == request.user or board.members.filter(id=request.user.id).exists()
            except Board.DoesNotExist:
                return False
        
        return True