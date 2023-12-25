import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from . import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ws_demo.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(routings.websocket_urlpatterns),
})
