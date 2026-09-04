import os
import datetime
from logging.handlers import WatchedFileHandler

"""
实例化：
    Filterer
    Handler
    StreamHandler
    logging.FileHandler

    WatchedFileHandler（简单文件是否删除、改变）
    MyTimedRotatingFileHandler
    
写日志：
    
"""
class MyTimedRotatingFileHandler(WatchedFileHandler):
    """ 支持每天创建一个日志 """

    def __init__(self, file_path, mode='a', encoding=None, delay=False, errors=None):

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.file_path = file_path
        self.file_name = "{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d"))

        # /logs/2021-5-9.log
        file_name = os.path.join(file_path, self.file_name)

        super().__init__(file_name, mode=mode, encoding=encoding, delay=delay, errors=errors)

    def emit(self, record):

        # 根据当前日期创建文件
        current_file_name = "{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d"))

        # 文件名不相等：新建文件 + 重新打开 + 重新读取os.state
        if current_file_name != self.file_name:
            self.file_name = current_file_name
            # 重新赋值，当前的文件名应该是最新的日期。  5-21.log
            self.baseFilename = os.path.abspath(os.path.join(self.file_path, current_file_name))

            if self.stream:
                self.stream.flush()
                self.stream.close()
            self.stream = self._open()
            self._statstream()

        # 文件名相等，当文件被删除 or 文件内容被修改，则重新打开文件。（可以注释，父类中已有）
        self.reopenIfNeeded()

        super().emit(record)

