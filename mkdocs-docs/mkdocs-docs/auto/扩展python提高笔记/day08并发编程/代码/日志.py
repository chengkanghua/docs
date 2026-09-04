import os
import time
import logging.config


def init_logger():
    # 1. 定义字典
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,  # 删除已存在其他日志的Handler
        'formatters': {
            'standard': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            }
        },
        'handlers': {
            'error_file': {
                # "class": 'logging.handlers.TimedRotatingFileHandler',
                "class": 'utils.custom.MyTimedRotatingFileHandler',
                'formatter': 'standard',
                'filename': "error.log",
                'when': 'M',  # 根据天拆分日志
                'interval': 1,  # 1天
                'backupCount': 30,  # 保留备份
                "encoding": "utf-8"
            }
        },
        'loggers': {
            'error': {
                'handlers': ['error_file', ],
                'level': 'ERROR',
                'propagate': False
            }
        },
    }

    # 2. 根据自定对logging进行配置
    logging.config.dictConfig(LOGGING_CONFIG)


def func():
    while True:
        time.sleep(0.5)
        logger_object = logging.getLogger("error")
        logger_object.error("123123")



if __name__ == '__main__':
    init_logger()
    func()
