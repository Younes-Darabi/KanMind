from rest_framework import serializers

from boards.models import Board
from users.models import User
from tasks.models import Comment, Task


class UserMinSerializer(serializers.ModelSerializer):
    """Simple serializer for User basic info."""

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskSerializer(serializers.ModelSerializer):

    assignee = UserMinSerializer(read_only=True)
    reviewer = UserMinSerializer(read_only=True)
    
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer', write_only=True, required=False, allow_null=True
    )
    
    comments_count = serializers.SerializerMethodField()
    
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 
            'priority', 'assignee', 'assignee_id', 'reviewer', 
            'reviewer_id', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):

        return obj.comments.count()

    def validate(self, data):

        instance = self.instance
        if instance and 'board' in data and data['board'] != instance.board:
            raise serializers.ValidationError({"board": "Das Ändern der Board-Id ist nicht erlaubt!"})

        board = data.get('board') or (instance.board if instance else None)
        
        if not board:
            raise serializers.ValidationError({"board": "Board is required."})

        assignee = data.get('assignee') or (instance.assignee if instance else None)
        reviewer = data.get('reviewer') or (instance.reviewer if instance else None)

        if assignee and not board.members.filter(id=assignee.id).exists() and board.owner != assignee:
            raise serializers.ValidationError({"assignee_id": "User must be a board member."})
        
        if reviewer and not board.members.filter(id=reviewer.id).exists() and board.owner != reviewer:
            raise serializers.ValidationError({"reviewer_id": "User must be a board member."})
        
        return data
    
    def to_representation(self, instance):

        representation = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            representation.pop('board', None)
            
        return representation


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