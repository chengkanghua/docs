import logging
import logging.handlers
import config


class LogHandle(object):
    """日志处理工具类"""

    def __init__(self, name=None, filename=None):
        self.name = config.LOGGING.get("name", "pytest")
        if name:
            self.name = name

        self.filename = config.LOGGING.get("filename", None)
        if filename:
            self.filename = filename

        self.charset = config.LOGGING.get("charset", "utf-8")
        self.log_backup_count = config.LOGGING.get("backup_count", 31)
        self.when = config.LOGGING.get("when", "d")

    def get_logger(self):
        # 创建logger，如果参数name表示日志器对象名，name为空则返回root logger
        logger = logging.getLogger(self.name)
        # 务必设置一个初始化的日志等级
        logger.setLevel(logging.DEBUG)
        # 这里进行判断，如果logger.handlers列表为空则添加，否则多次调用log日志函数会重复添加
        if not logger.handlers:
            # 创建handler
            fh = logging.handlers.TimedRotatingFileHandler(
                filename=self.filename,
                when=self.when,
                backupCount=self.log_backup_count,
                encoding=self.charset
            )
            sh = logging.StreamHandler()

            # 单独设置logger日志等级
            fh.setLevel(logging.INFO)
            # 设置输出日志格式
            simple_formatter = logging.Formatter(
                fmt="{levelname} {name} {module}:{lineno} {message}",
                style="{"
            )
            verbose_formatter = logging.Formatter(
                fmt="{levelname} {asctime} {name} {pathname}:{lineno} {message}",
                datefmt="%Y/%m/%d %H:%M:%S",
                style="{"
            )

            # 为handler指定输出格式
            fh.setFormatter(verbose_formatter)
            sh.setFormatter(simple_formatter)
            # 为logger添加的日志处理器
            logger.addHandler(fh)
            logger.addHandler(sh)

        return logger  # 直接返回logger

if __name__ == '__main__':
    from datetime import datetime

    log = LogHandle()
    log.filename = "../logs/pytest.log"
    logger = log.get_logger()
    logger.debug("日期测试")
    logger.info("普通日志")
    logger.warning("警告日志")
    logger.error("错误日志")
    logger.fatal("致命错误信息")
