# chat/routing.py
from django.urls import re_path

from . import consumers

#web socket routing 
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/artchat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
