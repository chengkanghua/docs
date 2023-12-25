import os
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
            },
            'simple': {
                'format': '%(levelname)s %(message)s',
                'style': '%',
            },
            'test': {
                'format': '$levelname $message',
                'style': '$',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'sms_file': {
                "class": 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join('logs', 'sms.log'),
                'maxBytes': 10240,  # 根据文件大小拆分日志
                'backupCount': 30,  # 备份个数
                "encoding": "utf-8"
            },
            'error_file': {
                "class": 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join('logs', "error.log"),
                'when': 'D',  # 根据天拆分日志
                'interval': 1,  # 1天
                'backupCount': 3,  # 保留备份
                "encoding": "utf-8"
            }
        },
        'loggers': {
            'sms': {
                'handlers': ['sms_file', ],  # 意味着通过sms的loggers，写日志时，级别》info 且 会写入到sms_file文件中。
                'level': "INFO",
                'propagate': False  # 通过sms写日志时，同时也会找到他的父亲。
            },
            'error': {
                'handlers': ['error_file'],
                'level': 'ERROR',
                'propagate': False
            }
        },
        'root': {
            'handlers': ['console', ],
            'level': 'ERROR',
            'propagate': True
        },
    }

    # 2. 根据自定对logging进行配置
    logging.config.dictConfig(LOGGING_CONFIG)


def func():
    try:
        int("asdf")
    except Exception as e:
        logger_object = logging.getLogger("error")
        logger_object.error(str(e))


if __name__ == '__main__':
    init_logger()
    func()
