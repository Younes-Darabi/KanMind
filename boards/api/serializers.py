from rest_framework import serializers

from boards.models import Board
from tasks.models import Task
from users.models import User


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for Board listing.
    Includes aggregated statistics like member count and task counts by status/priority.
    """

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:

        model = Board
        fields = ['id', 'title','members','member_count','ticket_count','tasks_to_do_count','tasks_high_prio_count','owner_id']
        extra_kwargs = {
            'members': {'write_only': True} 
        }

    def get_member_count(self, obj):
        """Returns the total number of members in the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns the total number of tasks assigned to this board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Returns the count of tasks with 'To-Do' status."""
        return obj.tasks.filter(status=Task.Status.TODO).count()

    def get_tasks_high_prio_count(self, obj):
        """Returns the count of tasks marked as 'High' priority."""
        return obj.tasks.filter(priority=Task.Priority.HIGH).count()
    

class UserMinSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer for User model to be used in nested representations.
    Provides only essential information: id, email, and fullname.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
    

class SingleBoardSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a single Board instance.
    Includes nested member data and associated tasks.
    """

    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:

        model = Board
        fields = ['id', 'title','owner_id','members','tasks']
        extra_kwargs = {
            'members': {'required': False} 
        }

    def to_representation(self, instance):
        """
        Overriding to convert member IDs into detailed user objects 
        using UserMinSerializer for the final JSON output.
        """

        representation = super().to_representation(instance)
        representation['members'] = UserMinSerializer(instance.members.all(), many=True).data
        return representation