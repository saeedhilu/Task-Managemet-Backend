from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from core.utils.permissions import AdminOrPm
from rest_framework.response import Response
from rest_framework import status
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AdminOrPm]

    def create(self, request, *args, **kwargs):
        data = request.data
        print('datais :',data)
        data['created_by'] = request.user.id  # Ensure created_by is set with the current user's ID

        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import  filters

from rest_framework import filters, generics
from rest_framework.response import Response
from .serializers import ProjectSearchSerializer
class ProjectSearchView(generics.ListAPIView):
    """
    API view to search for users by username.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name__startswith']  

    def get_queryset(self):
        project = self.request.query_params.get('q', '').lower()  # Convert to lowercase for case-insensitivity
        if len(project) > 4:
            return super().get_queryset().filter(name__icontains=project)[:7]
        else:
            return super().get_queryset().filter(name__istartswith=project)[:7]


    def get(self, request, *args, **kwargs):
        project = self.get_queryset().values('id', 'name')
        return Response({
            'results': list(project)
        })