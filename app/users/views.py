from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from .serializers import *
from users.models import CustomUser    
from .models import Task

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
                "refresh": tokens['refresh']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
