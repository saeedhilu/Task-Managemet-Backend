from rest_framework import serializers
from users.models import CustomUser
from tasks.models import Task, Tag
from rest_framework import serializers
from .models import Task
from users.models import CustomUser
from projects.models import Project  


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    
    """
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), many=True
    )
    members_usernames = serializers.SerializerMethodField()
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "assigned_to",
            "members_usernames",
            "created_by_email",
            "project",
        ]

    def get_members_usernames(self, obj):
        """
        Retrieve the usernames of the users assigned to the task.
        
        """

        member_ids = obj.assigned_to.all().values_list("id", flat=True)
        return CustomUser.objects.filter(id__in=member_ids).values_list(
            "username", "id"
        )

    def create(self, validated_data):
        
        validated_data["created_by"] = self.context["request"].user

        assigned_users = validated_data.pop("assigned_to", [])
        task = Task.objects.create(**validated_data)
        task.assigned_to.add(*assigned_users)
        task.save()
        task.notify_assigned_members()
        return task


class TaskSpecificSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    
    """
    assigned_to = serializers.StringRelatedField(many=True)
    project = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    
    """
    class Meta:
        model = Tag
        fields = "__all__"
