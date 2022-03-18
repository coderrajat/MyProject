"""
ASGI config for mayani project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayani.settings')
django.setup()

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import re_path,path

from django.core.asgi import get_asgi_application


from admins import consumers as admins_consumer
#from users import consumers as user_consumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    
    "websocket":AuthMiddlewareStack(
                    URLRouter(
                    [path(r'^notifications/(?P<stream>\w+)/$',admins_consumer.NotificationConsumer.as_asgi()),
                    #path(r'notifications/(?P<stream>\w+)/$',user_consumer.NotificationConsumer.as_asgi()),
                    ]
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
