import yaml
from logger import LogHandle


class Yaml(object):
    """yaml操作工具类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print("创建Yaml的单例")
            cls.__instance = super(Yaml, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.logger = LogHandle().get_logger()

    def read(self, path):
        """读取yaml文件"""
        with open(path, encoding="utf-8") as f:
            result = f.read()
            if result:
                result = yaml.load(result, Loader=yaml.FullLoader)
            return result

    def write(self, path, data):
        """写入yaml文件"""
        try:
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, Dumper=yaml.SafeDumper, allow_unicode=True)
            return True
        except Exception as e:
            self.logger(f"写入数据到yaml文件失败：{e}")
            return False


if __name__ == '__main__':
    ya = Yaml()
    data = ya.read("../demo/yaml_demo/data.yaml")
    print(data, type(data))
