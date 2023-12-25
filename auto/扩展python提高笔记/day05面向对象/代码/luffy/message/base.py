class BaseMessage(object):

    def send(self):
        """ 约束所有子类必须实现send方法 """
        raise NotImplementedError()
