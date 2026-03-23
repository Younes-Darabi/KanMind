from rest_framework import permissions


class IsOnlyOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to perform 
    specific actions (like Update or Delete).
    
    Rule:
    - If the user making the request is the 'owner' of the object, return True.
    - Otherwise, return False (Access Denied).
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requester is the owner of the board/task.
        """
        # Checks if the 'owner' attribute of the object matches the current user
        return obj.owner == request.user