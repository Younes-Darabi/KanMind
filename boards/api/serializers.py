from rest_framework import serializers
from boards.models import Board
from tasks.api.serializers import TaskSerializer
from tasks.models import Task
from users.models import User

class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for listing multiple boards.
    Provides aggregated statistics like member count and task summaries.
    """
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'members', 'member_count', 
            'ticket_count', 'tasks_to_do_count', 
            'tasks_high_prio_count', 'owner_id'
        ]
        extra_kwargs = {
            'members': {'write_only': True} # Hide member IDs in list view for cleaner output
        }

    def get_member_count(self, obj):
        """Calculates the total number of members in the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Calculates the total number of tasks (tickets) in the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Counts only the tasks that are in the 'To Do' state."""
        return obj.tasks.filter(status=Task.Status.TODO).count()

    def get_tasks_high_prio_count(self, obj):
        """Counts only the tasks marked with 'High' priority."""
        return obj.tasks.filter(priority=Task.Priority.HIGH).count()
    

class UserMinSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer for User model to return minimal info 
    in nested board representations.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
    

class SingleBoardSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a single board instance.
    Includes full task details and detailed member information.
    """
    owner_id = serializers.ReadOnlyField(source='owner.id')
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
        extra_kwargs = {
            'members': {'required': False} 
        }

    def to_representation(self, instance):
        """
        Customizes the JSON output to replace member IDs with 
        full member details using UserMinSerializer.
        """
        representation = super().to_representation(instance)
        representation['members'] = UserMinSerializer(instance.members.all(), many=True).data
        return representation
    

class BoardPatchSerializer(serializers.ModelSerializer):
    """
    Serializer used specifically for partial updates (PATCH) of a board.
    Validates input fields and manages member updates.
    """
    owner_data = UserMinSerializer(source='owner', read_only=True)
    members_data = UserMinSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members', 'members_data']
        extra_kwargs = {
            'members': {'write_only': True, 'required': False},
            'title': {'required': False}
        }

    def validate(self, attrs):
        """
        Strict validation to reject any undefined fields in the request body.
        """
        input_keys = self.initial_data.keys()
        allowed_keys = self.fields.keys()
        for key in input_keys:
            if key not in allowed_keys:
                raise serializers.ValidationError(
                    {key: f"Invalid field."}
                )
        return attrs