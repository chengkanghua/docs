class Response(object):
    def __init__(self, status=False, error=None, data=None):
        """
        封装响应数据
        :param status: 状态
        :param error: 错误信息
        :param data: 数据
        """
        self.status = status
        self.error = error
        self.data = data

    @property
    def dict(self):
        return self.__dict__


def do():
    """ 下载图片，可能失败，也可能成功。如果失败，返回错误信息；如果成功，则返回保存到本地的路径"""
    info = Response()
    try:
        info.status = True
        info.data = [11, 22, 33]
    except Exception as e:
        info.error = str(e)
    return info


def run():
    ret = do()  # 对象类型
    print(ret.status)
    print(ret.data)

    print(ret.dict)  # 字典


if __name__ == '__main__':
    run()
