class Message(object):
    """ 以后让所有发送消息的类，都继承Message """

    def send(self):
        """ 发送消息 """
        # 抛出异常
        raise NotImplementedError()


class WechatMessage(Message):
    def send(self):
        print("发送微信")


class DingDingMessage(Message):
    def send(self):
        print("发送钉钉")


obj = DingDingMessage()
obj.send()
