from .base import BaseMessage


class MaiMai(BaseMessage):
    def send(self):
        print("发送脉脉消息")
