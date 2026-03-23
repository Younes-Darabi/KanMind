from rest_framework import permissions

from boards.models import Board
from tasks.models import Task


class IsBoardMember(permissions.BasePermission):
    """
    Custom permission to ensure only board members or owners 
    can interact with tasks within that board.
    """

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check:
        - DELETE: Only Task Creator or Board Owner can delete a task.
        - OTHER: Any board member can view/edit.
        """

        user = request.user
        
        if request.method == 'DELETE':
            # Strict rule: Only the one who made the task or the boss (Board Owner)
            return obj.creator == user or obj.board.owner == user
        
        # General Access: Must be the owner or a team member
        return obj.board.owner == user or obj.board.members.filter(id=user.id).exists()

    def has_permission(self, request, view):
        """
        Global permission check: 
        Ensures the user belongs to the board before they can even 
        try to access or create tasks.
        """

        user = request.user

        # Scenario 1: Accessing a specific task via URL (e.g., for comments)
        task_id = view.kwargs.get('task_id')
        if task_id:
            try:
                task = Task.objects.get(pk=task_id)
                board = task.board
                return board.owner == user or board.members.filter(id=user.id).exists()
            except Task.DoesNotExist:
                return False

        # Scenario 2: Creating a new task (Board ID is in the request body)
        board_id = request.data.get('board')
        if board_id:
            try:
                board = Board.objects.get(pk=board_id)
                return board.owner == user or board.members.filter(id=user.id).exists()
            except Board.DoesNotExist:
                return False


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