from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from core.utils.permissions import AdminOrPm
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AdminOrPm]    