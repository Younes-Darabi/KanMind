from rest_framework import permissions

class IsBoardMember(permissions.BasePermission):
    """
    Permission to check if the user is a member or owner of the associated board.
    Works for both Task objects (obj.board) and Comment objects (obj.task.board).
    """
    
    def has_object_permission(self, request, view, obj):
        # Determine the board based on the object type (Task or Comment)
        board = obj.board if hasattr(obj, 'board') else obj.task.board
        
        # Access is granted if the user is the board owner or in the members list
        return board.owner == request.user or board.members.filter(id=request.user.id).exists()

class IsTaskDeletePermission(permissions.BasePermission):
    """
    Specific permission for deleting tasks.
    Only the task creator or the board owner is authorized to delete a task.
    """

    def has_object_permission(self, request, view, obj):
        # Allow deletion only for the creator of the task or the owner of the board
        return obj.creator == request.user or obj.board.owner == request.user

class IsCommentAuthor(permissions.BasePermission):
    """
    Object-level permission to ensure only the author of a comment 
    can modify or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the authenticated user is the actual author of the comment
        return obj.author == request.user