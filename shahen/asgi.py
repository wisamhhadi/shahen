# shahen/asgi.py - FIXED VERSION

import os
import django
from django.core.asgi import get_asgi_application

# Set Django settings FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shahen.settings')

# THEN setup Django
django.setup()

# Get Django ASGI app
django_asgi_app = get_asgi_application()

# Import channels components AFTER Django setup
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from core.consumer import ChatConsumer, NotificationConsumer, CaptainChatConsumer, UserChatConsumer

# WebSocket URL patterns
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/captainchat/(?P<room_id>\w+)/$', CaptainChatConsumer.as_asgi()),
    re_path(r'ws/userchat/(?P<room_id>\w+)/$', UserChatConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]

# ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})