from rest_framework import serializers
from users.models import CustomUser
from tasks.models import Task,Tag


from rest_framework import serializers
from .models import Task
from users.models import CustomUser
from projects.models import Project  # Assuming Project is in a separate app

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), many=True
    )
    members_usernames = serializers.SerializerMethodField()
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'assigned_to', 'members_usernames', 'created_by_email', 'project']


    def get_members_usernames(self, obj):
        # Fetching usernames of members from the related users
        member_ids = obj.assigned_to.all().values_list('id', flat=True)
        print('members are', member_ids)
        return CustomUser.objects.filter(id__in=member_ids).values_list('username', flat=True)
    
    def create(self, validated_data):
        # Automatically set the created_by field to the requesting user
        print('validate dat is:', validated_data)
        validated_data['created_by'] = self.context['request'].user

        # Handle Many-to-Many field for assigned_to
        assigned_users = validated_data.pop('assigned_to', [])
        task = Task.objects.create(**validated_data)
        task.assigned_to.add(*assigned_users)
        task.save()
        task.notify_assigned_members()
        return task
    
class TaskSpecificSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField(many=True)  
    project = serializers.StringRelatedField()  

    class Meta:
        model = Task
        fields = '__all__'

    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        