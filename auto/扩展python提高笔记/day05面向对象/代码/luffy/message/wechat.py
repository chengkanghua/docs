from .base import BaseMessage


class Wechat(BaseMessage):
    def send(self):
        print("发送微信")
