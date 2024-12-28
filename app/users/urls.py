from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "comment/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="task-list-create",
    ),
    path(
        "comment/<int:pk>/",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="task-detail",
    ),
    path(
        "mention/",
        MentionViewSet.as_view({"get": "list", "post": "create"}),
        name="task-list-create",
    ),
    path(
        "mention/<int:pk>/",
        MentionViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="task-detail",
    ),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("users-search/", UserSearchView.as_view(), name="user-search"),
    path("summary-statics/", AllStatsView.as_view(), name="list-all-statics"),
    path("task-useres/<int:task_id>/", TaskUsersView.as_view(), name="task-users"),
]
