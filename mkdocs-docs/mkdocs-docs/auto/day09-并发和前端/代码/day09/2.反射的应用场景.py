import importlib
import settings


def run():
    # 很多的业务代码....
    # "utils.f1",
    for path in settings.SEND_LIST:
        module_path_string, func_str = path.rsplit('.', maxsplit=1)
        # 以字符串的形式导入模块
        m = importlib.import_module(module_path_string)
        func = getattr(m, func_str)
        func()


if __name__ == '__main__':
    run()
