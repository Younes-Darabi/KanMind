from rest_framework import permissions


class IsBoardMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        board = obj.board if hasattr(obj, 'board') else obj.task.board
        return board.owner == request.user or board.members.filter(id=request.user.id).exists()

class IsTaskDeletePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or obj.board.owner == request.user

class IsCommentAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user