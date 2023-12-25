""" 系统启动文件 """
import os


def init():
    """ 项目加载所必备的功能"""
    pass


def run():
    # 通过环境变量告诉代码，用户配置文件写在了什么地方？
    os.environ.setdefault("CRM_SETTINGS_PATH", "crm.user_settings")

    # 项目加载
    init()

    # 想要读取所有的配置文件
    from conf import settings
    print(settings.HOST)
    print(settings.PORT)
    print(settings.DATA)


if __name__ == '__main__':
    run()
