from rest_framework import permissions


class IsBoardMemberOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or obj.members.filter(id=request.user.id).exists()
    

class IsOnlyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user