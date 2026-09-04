from .base import BaseMessage


class DingDing(BaseMessage):
    def send(self):
        print("发送钉钉")
