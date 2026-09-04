"""
ASGI config for ws_demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from ws_demo import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ws_demo.settings')

#
# application = get_asgi_application()

# 支持http和websocket
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 自动找urls.py，找视图函数  --> http
    "websocket": URLRouter(routings.websocket_urlpatterns),  # routings(urls）、consumers（views）
})
