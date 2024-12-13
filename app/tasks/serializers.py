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
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        # Automatically set the created_by field to the requesting user
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
        