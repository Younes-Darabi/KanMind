from rest_framework import serializers

from users.models import User
from tasks.models import Comment, Task


class UserMinSerializer(serializers.ModelSerializer):
    """Simple serializer for User basic info."""

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskSerializer(serializers.ModelSerializer):
    """
    Handles Task serialization with nested user data for display 
    and primary keys for writing operations.
    """
    # For Displaying (Read-only)
    assignee = UserMinSerializer(read_only=True)
    reviewer = UserMinSerializer(read_only=True)
    
    # For Writing (Write-only) - accepts IDs from frontend
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee', write_only=True, required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer', write_only=True, required=False
    )
    comments_count = serializers.IntegerField(read_only=True, default=0)
    board = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 
            'priority', 'assignee', 'assignee_id', 'reviewer', 
            'reviewer_id', 'due_date', 'comments_count'
        ]

    def validate(self, data):
        """
        Ensures that the assigned user and reviewer are actually 
        members of the board associated with the task.
        """
        
        instance = self.instance
        board = data.get('board', instance.board if instance else None)
        
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError({"assignee_id": "User must be a board member."})
        
        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError({"reviewer_id": "User must be a board member."})
        
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Task comments. 
    The author is automatically set to the logged-in user in the View.
    """
    
    author = serializers.ReadOnlyField(source='author.fullname')

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']