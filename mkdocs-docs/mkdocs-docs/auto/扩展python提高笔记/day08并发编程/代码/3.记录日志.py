import os
import time
import logging.config
from logging.handlers import TimedRotatingFileHandler

# 1. 定义字典
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,  # 删除已存在其他日志的Handler
    'formatters': {
        'standard': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'error_file': {
            # "class": 'logging.handlers.TimedRotatingFileHandler',
            "class": 'utils.luffy.LuffyTimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': 'a1.log',
            'when': 'D',  # 根据天拆分日志
            'interval': 1,  # 1天
            'backupCount': 3,  # 保留备份
            "encoding": "utf-8"
        }
    },
    'loggers': {
        'error': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': True
        }
    },
}

# 2. 根据自定对logging进行配置
logging.config.dictConfig(LOGGING_CONFIG)

while True:
    logger_object = logging.getLogger("error")
    logger_object.error('6666666666')
    time.sleep(1)
