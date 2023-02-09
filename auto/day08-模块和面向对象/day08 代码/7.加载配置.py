import configparser


class ConfigContext:
    def __init__(self):
        self.wx_url = str
        self.min_inventory = float
        self.pool_size = int
        self.max_error_count = int


def load_config():
    # 读取ini文件
    config = configparser.ConfigParser()
    config.read('settings.ini', encoding='utf-8')

    obj = ConfigContext()
    for k, convert in obj.__dict__.items():
        value = config.get('settings', k)
        target_type_value = convert(value)
        setattr(obj, k, target_type_value)

    return obj


def run():
    # 加载配置文件
    data_object = load_config()
    print(data_object.wx_url)
    print(data_object.pool_size, type(data_object.pool_size))


if __name__ == '__main__':
    run()
