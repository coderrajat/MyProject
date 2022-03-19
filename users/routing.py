from django.urls import re_path,path

from . import consumers
websocket_urlpatterns = [
    
        re_path(r'ws/user_notification/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r"ws/user_notification/(?P<stream>\w+)/$", consumers.NotificationConsumer.as_asgi()),
]