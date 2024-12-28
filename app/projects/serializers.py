from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User
from users.models import CustomUser

class ProjectSerializer(serializers.ModelSerializer):
    created_by_username = serializers.SerializerMethodField()
    members_usernames = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'created_by', 'created_by_username', 'members', 'members_usernames']

    def get_created_by_username(self, obj):
        print('hello')
        return obj.created_by.username if obj.created_by else None

    def get_members_usernames(self, obj):
        
        member_ids = obj.members.all().values_list('id', flat=True)
        print('members are', member_ids)
        return CustomUser.objects.filter(id__in=member_ids).values_list('id','username')


class ProjectSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name'] 