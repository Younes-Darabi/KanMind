from rest_framework import serializers
from users.models import User
from tasks.models import Task

class UserMinSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

class TaskSerializer(serializers.ModelSerializer):

    assignee = UserMinSerializer(read_only=True)
    reviewer = UserMinSerializer(read_only=True)
    

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
        
        instance = self.instance
        board = data.get('board', instance.board if instance else None)
        
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError({"assignee_id": "User must be a board member."})
        
        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError({"reviewer_id": "User must be a board member."})
        
        return data