import os
import importlib
from commons import global_settings


class Settings(object):
    def __init__(self):
        # 读取所有的全局配置
        """
            HOST = "1.1.1.1"
            PORT = 80
            NAME = "alex"
        """
        for name in dir(global_settings):
            # 排除那些非大写的值
            if not name.isupper():
                continue
            value = getattr(global_settings, name)  # global_settings.HOST
            setattr(self, name, value)

        # 用户配置
        user_settings_path = os.environ.get("CRM_SETTINGS_PATH") # "crm.user_settings"
        m = importlib.import_module(user_settings_path)

        for name in dir(m):
            # 排除那些非大写的值
            if not name.isupper():
                continue
            value = getattr(m, name)  # m.HOST    m.DATA
            setattr(self, name, value)




settings = Settings()
