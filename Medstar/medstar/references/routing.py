from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'doctor/(?P<next_doctor_id>\d+)/', consumers.ReferenceConsumer.as_asgi()),
]