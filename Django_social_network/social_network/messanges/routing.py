from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<sender_id>\d+)/(?P<addressee_id>\d+)/', consumers.ChatConsumer.as_asgi()),
    re_path(r'group/(?P<group_id>\d+)/', consumers.ChatGroupConsumer.as_asgi()),
]