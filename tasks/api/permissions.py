from rest_framework import permissions
from boards.models import Board
from tasks.models import Task


class IsBoardMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user
        
        if request.method == 'DELETE':
            return obj.creator == user or obj.board.owner == user
        
        return obj.board.owner == user or obj.board.members.filter(id=user.id).exists()

    def has_permission(self, request, view):
        user = request.user
        
        task_id = view.kwargs.get('task_id')
        if task_id:
            try:
                task = Task.objects.get(pk=task_id)
                board = task.board
                return board.owner == user or board.members.filter(id=user.id).exists()
            except Task.DoesNotExist:
                return False

        board_id = request.data.get('board')
        if board_id:
            try:
                board = Board.objects.get(pk=board_id)
                return board.owner == user or board.members.filter(id=user.id).exists()
            except Board.DoesNotExist:
                return False


class IsCommentAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.method == 'DELETE':
            return obj.author == request.user
        
        return True