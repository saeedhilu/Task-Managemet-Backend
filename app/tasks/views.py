from django.shortcuts import render
from .models import Task
from rest_framework import status,viewsets
from .serializers import *
from core.utils.permissions import IsAdminAndAuthenticated,AdminOrPm

from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # Allow only authenticated users to access and admins to create
    permission_classes = [AdminOrPm]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AdminOrPm]

from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import viewsets

class TaskSpecificViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSpecificSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.request.query_params.get('user_email')  
        status = self.request.query_params.get('status')  
        print('user email and status', email, status)

        queryset = super().get_queryset()

        if email:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                queryset = queryset.filter(Q(assigned_to=user) | Q(created_by=user)).distinct()

        if status:
              queryset = queryset.filter(status=status, assigned_to__email=email) 
        
        return queryset
