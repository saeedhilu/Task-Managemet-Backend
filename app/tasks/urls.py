from django.urls import path
from .views import *

urlpatterns = [

    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list-create'),  
    path('tasks/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='task-detail'),
    path('tags/', TagViewSet.as_view({'get': 'list', 'post': 'create'}), name='tag-list-create'),  
    path('taks-specific/', TaskSpecificViewSet.as_view({'get': 'list',}), name='tag-list'),  
    path('tags/<int:pk>/', TagViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='tag-detail'),
]
