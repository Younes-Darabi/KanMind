from rest_framework import permissions

class IsBoardMemberOrOwner(permissions.BasePermission):
    """
    Object-level permission to allow access only to the board's owner 
    or its authorized members.
    Used for general access like viewing or updating board details.
    """
    
    def has_object_permission(self, request, view, obj):
        """Grant access if the user is the owner OR exists in the members list"""
        return obj.owner == request.user or obj.members.filter(id=request.user.id).exists()
    

class IsOnlyOwner(permissions.BasePermission):
    """
    Strict object-level permission that limits access exclusively to the board owner.
    Typically used for sensitive operations like deleting the entire board.
    """

    def has_object_permission(self, request, view, obj):
        """Only the user who created the board (owner) is authorized"""
        return obj.owner == request.user