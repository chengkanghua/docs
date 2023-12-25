import importlib
from config import MESSAGE


def do_send_message():
    """
    MESSAGE = [
        "message.dingding.DingDing",
        "message.email.Email",
        "message.wechat.Wechat",
    ]
    :return:
    """
    for path in MESSAGE:
        module_path, cls_name = path.rsplit(".", maxsplit=1)
        m = importlib.import_module(module_path)
        cls = getattr(m, cls_name)
        obj = cls()
        obj.send()
