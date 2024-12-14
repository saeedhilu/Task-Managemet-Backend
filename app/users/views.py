from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from .serializers import *
from users.models import CustomUser    


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)        
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            tokens = user.tokens  
            return Response({
                "message": "Login successful.",
                "access": tokens['access'],
                "refresh": tokens['refresh'],
                "user": {
                    "email": user.email,  # Assuming you need user data
                    "username": user.username,  # Optional: add other user details as needed
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MentionViewSet(viewsets.ModelViewSet):
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer

    def perform_create(self, serializer):
        serializer.save(mentioned_by=self.request.user)



from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

class NotificationPagination(PageNumberPagination):
    page_size = 10

class NotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    

from rest_framework import  filters

from rest_framework import filters, generics
from rest_framework.response import Response

class UserSearchView(generics.ListAPIView):
    """
    API view to search for users by username.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username__startswith']  

    def get_queryset(self):
        username = self.request.query_params.get('q', '')
        if len(username) > 4:
            return super().get_queryset().filter(username__icontains=username)[:7] 
        else:
            return super().get_queryset().filter(username__startswith=username)[:7]

    def get(self, request, *args, **kwargs):
        users = self.get_queryset().values('id', 'username')
        return Response({
            'results': list(users)
        })
