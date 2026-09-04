from django.urls import path
from channels.routing import URLRouter
from .consumer import SSHCmdConsumer
# 由于我们可能会对websocket请求进行一些验证或者身份认证，所以我们在consumer应用下面在创建一个middleware文件，里面可以配置一些认证规则
ws_router = URLRouter([
        path('ws/ssh/<int:id>/', SSHCmdConsumer),
    ])