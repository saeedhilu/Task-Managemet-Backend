# config/routing.py
from django.urls import path
from tasks.consumers import NotificationConsumer

websocket_urlpatterns = [
    path("auth/ws/notifications/", NotificationConsumer.as_asgi()),
]
