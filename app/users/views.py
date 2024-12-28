from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters, generics
from .serializers import *
from users.models import CustomUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from core.utils.pagination import CommentPagination, NotificationPagination
from projects.models import Project
from tasks.models import Task
from django.utils import timezone
from core.utils.permissions import AdminOrPm
from rest_framework.exceptions import NotFound


class RegisterView(APIView):
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.validated_data["email"])
            tokens = user.tokens
            return Response(
                {
                    "message": "Login successful.",
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                    "user": {
                        "email": user.email,
                        "username": user.username,
                        "user_id": user.id,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db import transaction

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating, retrieving, updating, and deleting comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # pagination_class = CommentPagination

    def get_queryset(self):
        query_set = super().get_queryset()
        task_id = self.request.query_params.get("taskId")

        if task_id:
            return query_set.filter(task_id=task_id)
        return query_set

    def perform_create(self, serializer):
        # Save the comment
        comment = serializer.save(created_by=self.request.user)

        # Detect mentions in the comment text
        mentioned_usernames = self.detect_mentions(comment.text)
        print('mentioned_usernames', mentioned_usernames)
        # Save mentions and send notifications
        self.handle_mentions(mentioned_usernames, comment)

    def detect_mentions(self, text):
        """
        Extract mentioned usernames from the comment text using the @ prefix.
        """
        import re
        return re.findall(r'@(\w+)', text)

    def handle_mentions(self, mentioned_usernames, comment):
        mentioned_users = set()
        invalid_usernames = []

        # Fetch users in a single query
        existing_users = CustomUser.objects.filter(username__in=mentioned_usernames)
        existing_usernames = {user.username for user in existing_users}

        # Identify invalid usernames
        invalid_usernames = set(mentioned_usernames) - existing_usernames
        mentioned_users.update(existing_users)

        # Log invalid usernames
        if invalid_usernames:
            print(f"Invalid usernames: {', '.join(invalid_usernames)}")

        # Create the Mention object and assign mentioned users
        if mentioned_users:
            print('mention udn')
            with transaction.atomic():  # Ensure atomic transaction
                mention = Mention.objects.create(
                    task=comment.task,
                    mentioned_by=self.request.user
                )
                mention.mentioned_user.set(mentioned_users)  # Use .set() here for bulk assignment

                # Send notifications
                self.send_mention_notification(mentioned_users, comment)


    def send_mention_notification(self, mentioned_users, comment):
        """
        Send notifications to mentioned users.
        """
        from django.core.mail import send_mail

        for user in mentioned_users:
            try:
                send_mail(
                    subject="You were mentioned in a task",
                    message=(
                        f"Hello {user.username},\n\n"
                        f"You were mentioned by {comment.created_by.username} in task '{comment.task.title}'.\n"
                        f"Click here to view the task: http://example.com/tasks/{comment.task.id}/\n\n"
                        "Thank you,\nYour Team"
                    ),
                    from_email='noreply@example.com',
                    recipient_list=[user.email],
                )
            except Exception as e:
                print(f"Failed to send email to {user.email}: {str(e)}")




class MentionViewSet(viewsets.ModelViewSet):
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer

    def perform_create(self, serializer):
        serializer.save(mentioned_by=self.request.user)


class NotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class UserSearchView(generics.ListAPIView):
    """
    API view to search for users by username.
    """

    queryset = CustomUser.objects.all()

    serializer_class = UserSearchSerializer
    filter_backends = [filters.SearchFilter]

    search_fields = ["username__startswith"]

    def get_queryset(self):
        username = self.request.query_params.get("q", "")
        if len(username) > 4:
            return super().get_queryset().filter(username__icontains=username)[:7]
        else:
            return super().get_queryset().filter(username__startswith=username)[:7]

    def get(self, request, *args, **kwargs):

        users = self.get_queryset().values("id", "username")
        return Response({"results": list(users)})


class TaskUsersView(ListAPIView):
    """
    API view to get users assigned to a task.

    """

    serializer_class = UserSearchSerializer

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task not found.")
        return task.assigned_to.all()
    




class AllStatsView(APIView):
    permission_classes = [AdminOrPm]

    def get(self, request, *args, **kwargs):
        total_projects = Project.objects.count()
        total_tasks = Task.objects.count()
        total_users = CustomUser.objects.count()
        completed_projects = Project.objects.filter(status="completed").count()

        return Response(
            {
                "total_projects": total_projects,
                "total_tasks": total_tasks,
                "total_users": total_users,
                "completed_projects": completed_projects,
            }
        )
