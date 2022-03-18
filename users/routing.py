from django.urls import re_path,path

from . import consumers as user_consumer
websocket_urlpatterns = [
    
        path(r"notifications/(?P<stream>\w+)/$", user_consumer.NotificationConsumer.as_asgi())

]