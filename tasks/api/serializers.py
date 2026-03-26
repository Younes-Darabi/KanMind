from rest_framework import serializers

from boards.models import Board
from users.models import User
from tasks.models import Comment, Task


class UserMinSerializer(serializers.ModelSerializer):

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
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), required=True)

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
        input_keys = set(self.initial_data.keys())
        allowed_keys = set(self.fields.keys())
        extra_keys = input_keys - allowed_keys
        if extra_keys:
            raise serializers.ValidationError({key: "Invalid field." for key in extra_keys})
        if self.instance and 'board' in self.initial_data:
             raise serializers.ValidationError({"board": "Changing the board ID is not allowed."})
        board = self.instance.board if self.instance else data.get('board')
        for field in ['assignee', 'reviewer']:
            user = data.get(field)
            if user and not (board.members.filter(id=user.id).exists() or board.owner == user):
                raise serializers.ValidationError({f"{field}_id": "User must be a board member."})
        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            representation.pop('board', None)
        return representation


class CommentSerializer(serializers.ModelSerializer): 
    author = serializers.ReadOnlyField(source='author.fullname')

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']