"""
ASGI config for mayani project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from admins import consumers

from django.urls import re_path,path

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayani.settings')
import admins.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    
    "websocket":AuthMiddlewareStack(
                    URLRouter(
                    [path('admins/notification_testing/',consumers.NotificationConsumer.as_asgi())]
                ))
    
    
    
})

'''
"websocket":AuthMiddlewareStack(
                URLRouter(
                    admins.routing.websocket_urlpatterns
                )
            )

'''
#application = get_asgi_application()
