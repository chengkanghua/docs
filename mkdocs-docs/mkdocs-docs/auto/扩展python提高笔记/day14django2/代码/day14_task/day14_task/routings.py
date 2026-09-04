from django.urls import re_path

from app01 import consumers

websocket_urlpatterns = [
    re_path(r'audit/(?P<tid>\d+)/$', consumers.AuditConsumer.as_asgi()),
]
