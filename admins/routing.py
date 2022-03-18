from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path(r'^notifications/(?P<stream>\w+)/$', consumers.NotificationConsumer.as_asgi()), 

]