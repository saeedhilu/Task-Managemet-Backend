
import os

from django.core.asgi import get_asgi_application


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from .routing import websocket_urlpatterns
from  .middleware import BaseJWTAuthMiddleWare


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(BaseJWTAuthMiddleWare(URLRouter(websocket_urlpatterns))),
})