from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r"ws/notification/(?P<stream>\w+)/$", consumers.NotificationConsumer.as_asgi()),
]