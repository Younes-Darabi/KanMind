from rest_framework import permissions
from django.db.models import Q

from boards.models import Board
from tasks.models import Task


class IsBoardMember(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if request.method in ['GET', 'PATCH', 'DELETE'] and ('pk' in view.kwargs or 'comment_id' in view.kwargs):
            return True

        if request.method == 'POST':

            board_id = request.data.get('board')
            if board_id:
                return Board.objects.filter(id=board_id).filter(
                    Q(owner=user) | Q(members=user)
                ).exists()

            task_id = view.kwargs.get('task_id')
            if task_id:
                try:
                    task = Task.objects.get(pk=task_id)
                    return task.board.owner == user or task.board.members.filter(id=user.id).exists()
                except Task.DoesNotExist:
                    return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if hasattr(obj, 'board'):
            board = obj.board
        else:
            board = obj.task.board

        if request.method == 'DELETE' and hasattr(obj, 'creator'):
            return obj.creator == user or board.owner == user
        
        return board.owner == user or board.members.filter(id=user.id).exists()


class IsCommentAuthor(permissions.BasePermission):
    """
    Custom permission to ensure only the author of a comment 
    can perform destructive actions on it.
    """

    def has_object_permission(self, request, view, obj):
        
        # Anyone authorized can view or edit (if allowed by view), 
        # but only the author can DELETE.
        if request.method == 'DELETE':
            return obj.author == request.user
        
        return True