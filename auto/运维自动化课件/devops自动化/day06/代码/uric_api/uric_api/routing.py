from channels.routing import ProtocolTypeRouter, ChannelNameRouter

# ProtocolTypeRouter 根据不同的请求协议，分发到不同的协议处理系统，如果是websocket协议，那么自动找routing.ws_router进行路由转发，如果是channel，那么通过executors.SSHExecutor路由进行转发，如果是http协议，那么还是按照之前的方式进行分发
from host import ws_urls  # 这里类似原来的http编写代码时的路由，只是当时的路由信息，填写在了urls,而接下来，我们要编写websocket的路由，则写在routing，模块下

application = ProtocolTypeRouter({
    'websocket': ws_urls.ws_router
})