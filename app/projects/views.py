from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from core.utils.permissions import AdminOrPm
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework import filters, generics
from rest_framework.response import Response
from .serializers import ProjectSearchSerializer
from django.core.cache import cache


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing projects.

    """

    queryset = (
        Project.objects.select_related("created_by").prefetch_related("members").all()
    )

    serializer_class = ProjectSerializer
    permission_classes = [AdminOrPm]

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all projects.
        If the request contains a cache key for the current user, it retrieves the data from cache instead of making a database query.
        If the cache key is not found, it makes a database query, serializes the data, and stores it in cache before returning the response.
        Cache timeout is set to 300 seconds (5 minutes).

        """

        cache_key = f"project_list_user_{request.user.id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=300)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a new project.
        """

        data = request.data
        data["created_by"] = request.user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectSearchView(generics.ListAPIView):
    """
    API view to search for users by username.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name__startswith"]

    def get_queryset(self):
        """
        Returns a list of projects that start with the given query.
        If the query is longer than 4 characters, it uses `icontains` filter to search for projects that contain the query in the name.
        If the query is 4 characters or shorter, it uses `istartswith` filter to search for projects that start with the query in the name.
        Returns a maximum of 7 projects.

        """
        project = self.request.query_params.get("q", "").lower()
        if len(project) > 4:
            return super().get_queryset().filter(name__icontains=project)[:7]
        else:
            return super().get_queryset().filter(name__istartswith=project)[:7]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of projects that match the search query.
        """
        project = self.get_queryset().values("id", "name")
        return Response({"results": list(project)})
