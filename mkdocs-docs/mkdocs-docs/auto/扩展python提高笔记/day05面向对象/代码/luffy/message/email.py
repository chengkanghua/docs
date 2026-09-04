from .base import BaseMessage


class Email(BaseMessage):
    def send(self):
        print("发送邮件")
