from rest_framework import serializers
from boards.models import Board
from users.models import User
from tasks.models import Comment, Task

class UserMinSerializer(serializers.ModelSerializer):
    """
    Small serializer for User model to provide basic info 
    in nested task representations.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskSerializer(serializers.ModelSerializer):
    """
    Main serializer for Task management.
    Includes logic for read-only nested objects and write-only ID fields.
    """
    # Read-only fields to show full user details in GET requests
    assignee = UserMinSerializer(read_only=True)
    reviewer = UserMinSerializer(read_only=True)
    
    # Write-only fields to accept IDs when creating or updating
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer', write_only=True, required=False, allow_null=True
    )
    
    # Dynamically calculate the number of comments for each task
    comments_count = serializers.SerializerMethodField()
    
    # Required field to link task to a board
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), required=True)

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 
            'priority', 'assignee', 'assignee_id', 'reviewer', 
            'reviewer_id', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        """Returns the total number of comments associated with the task."""
        return obj.comments.count()

    def validate(self, data):
        """
        Custom validation logic for strict API requirements.
        """
        # 1. Strict Validation: Reject any fields not defined in the serializer
        input_keys = set(self.initial_data.keys())
        allowed_keys = set(self.fields.keys())
        extra_keys = input_keys - allowed_keys
        if extra_keys:
            raise serializers.ValidationError({key: "Invalid field." for key in extra_keys})
            
        # 2. Immutable Field: Prevent changing the board after task creation
        if self.instance and 'board' in self.initial_data:
             raise serializers.ValidationError({"board": "Changing the board ID is not allowed."})
             
        # 3. Membership Validation: Ensure assignee/reviewer are members of the task's board
        board = self.instance.board if self.instance else data.get('board')
        for field in ['assignee', 'reviewer']:
            user = data.get(field)
            if user and not (board.members.filter(id=user.id).exists() or board.owner == user):
                raise serializers.ValidationError({f"{field}_id": "User must be a board member."})
        
        return data
    
    def to_representation(self, instance):
        """
        Modify the output JSON. 
        Removes the 'board' field during PATCH requests as per documentation.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            representation.pop('board', None)
        return representation


class CommentSerializer(serializers.ModelSerializer): 
    """
    Serializer for Task comments.
    Ensures that the author is read-only and extracted from the user profile.
    """
    author = serializers.ReadOnlyField(source='author.fullname')

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']