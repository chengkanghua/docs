import logging
import traceback

# 1. 对日志进行配置
logging.basicConfig(
    filename='v1.log',  # 日志文件
    format='%(asctime)s :  %(message)s',  # 写日志时，文件的格式。
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=20  # 级别，以后只有大于20的级别时，才能真正日志内容写入到文件中。
)


def run():
    try:
        int("sfd")
    except Exception as e:
        logging.error(traceback.format_exc())  # 40,你傻呀


if __name__ == '__main__':
    run()
