from django.urls import path
from .views import *

urlpatterns = [

    path('project/', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-list-create'),  
    path('project/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='project-detail'),
    
]
