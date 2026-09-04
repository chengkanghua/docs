import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import WatchedFileHandler
from stat import ST_DEV, ST_INO, ST_MTIME

"""
在内容Logging模块：
    - 实例化 LuffyTimedRotatingFileHandler 对象
        Filterer
        Handler
        StreamHandler
        logging.FileHandler
        
        BaseRotatingHandler.__init__
        TimedRotatingFileHandler.__init__
        LuffyTimedRotatingFileHandler.__init__
        
        此过程：
            self.baseFilename     # 日志文件的绝对路径
            self.stream = stream  # 打开的文件对象
            
    - 写日志
        对象.emit("日志内容")
            def emit(self, record):
                try:
                    # 判断是否已经到了第2天，如果到了第2天，就重命名。
                    if self.shouldRollover(record):
                        self.doRollover()
                    
                    # 写日志
                    # 判断日志文件是否存在，如果不存在。【方案1：自己写；直接把logging中的功能拿过来】
                        self.stream = None
                        
                    logging.FileHandler.emit(self, record)
                except Exception:
                    self.handleError(record)
            
            
            def emit(self, record):
                try:
                    # 判断是否已经到了第2天，如果到了第2天，就重命名。
                    if self.shouldRollover(record):
                        self.doRollover()
                    
                    # 写日志
                    # 判断日志文件是否存在，如果不存在。【方案1：自己写；直接把logging中的功能拿过来】
                        self.stream = None
                        
                    logging.FileHandler.emit(self, record)
                except Exception:
                    self.handleError(record)
                    
            def emit(self, record):
                # 如果stream为空，重新打开文件
                if self.stream is None:
                    self.stream = self._open()
                StreamHandler.emit(self, record)
                
            def emit(self, record):    
                try:
                    msg = self.format(record)
                    stream = self.stream
                    stream.write(msg + self.terminator)
                    self.flush()
                except RecursionError:  # See issue 36272
                    raise
                except Exception:
                    self.handleError(record)
                
"""


class LuffyTimedRotatingFileHandler(TimedRotatingFileHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dev, self.ino = -1, -1
        self._statstream()

    def _statstream(self):
        if self.stream:
            sres = os.fstat(self.stream.fileno())
            self.dev, self.ino = sres[ST_DEV], sres[ST_INO]

    def reopenIfNeeded(self):
        """
        Reopen log file if needed.

        Checks if the underlying file has changed, and if it
        has, close the old stream and reopen the file to get the
        current stream.
        """
        # Reduce the chance of race conditions by stat'ing by path only
        # once and then fstat'ing our new fd if we opened a new log stream.
        # See issue #14632: Thanks to John Mulligan for the problem report
        # and patch.
        try:
            # stat the file by path, checking for existence
            sres = os.stat(self.baseFilename)
        except FileNotFoundError:
            sres = None
        # compare file system stat with that of our stream file handle
        if not sres or sres[ST_DEV] != self.dev or sres[ST_INO] != self.ino:
            if self.stream is not None:
                # we have an open file handle, clean it up
                self.stream.flush()
                self.stream.close()
                self.stream = None  # See Issue #21742: _open () might fail.
                # open a new file handle and get new stat info from that fd
                self.stream = self._open()
                self._statstream()
            else:
                self.stream = None

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)

        """
        # 文件名：a1-5-9.log
        dfn = self.rotation_filename(self.baseFilename + "." +time.strftime(self.suffix, timeTuple))
        # 判断是否存在
        if os.path.exists(dfn):
            os.remove(dfn)
        # 重命名
        self.rotate(self.baseFilename, dfn)
        """
        dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, timeTuple))
        if not os.path.exists(dfn):
            self.rotate(self.baseFilename, dfn)

        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def emit(self, record):
        try:
            # 判断是否已经到了第2天，如果到了第2天，就重命名。
            if self.shouldRollover(record):
                self.doRollover()

            # 写日志
            # 判断日志文件是否存在，如果不存在。【方案1：自己写；直接把logging中的功能拿过来】
            self.reopenIfNeeded()  # self.stream = None

            logging.FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)
