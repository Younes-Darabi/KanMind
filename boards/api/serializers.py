from rest_framework import serializers
from boards.models import Board
from tasks.models import Task


class BoardSerializer(serializers.ModelSerializer):

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
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status=Task.Status.TODO).count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority=Task.Priority.HIGH).count()