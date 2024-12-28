from django.shortcuts import render
from .models import Task
from rest_framework import status, viewsets
from .serializers import *
from core.utils.permissions import IsAdminAndAuthenticated, AdminOrPm
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import viewsets


class TaskViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [AdminOrPm]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing tags.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AdminOrPm]


class TaskSpecificViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing tasks for a specific user.

    """

    queryset = Task.objects.all()
    serializer_class = TaskSpecificSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter tasks based on user email and status query parameters.
        """
        email = self.request.query_params.get("user_email")
        status = self.request.query_params.get("status")

        queryset = super().get_queryset()

        if email:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                queryset = queryset.filter(
                    Q(assigned_to=user) | Q(created_by=user)
                ).distinct()

        if status:
            queryset = queryset.filter(status=status, assigned_to__email=email)

        return queryset
