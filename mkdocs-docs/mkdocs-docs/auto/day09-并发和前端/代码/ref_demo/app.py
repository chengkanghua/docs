import importlib
import settings


def run():
    # 很多其他逻辑

    # "commons.x1.db.EmailHelper",
    for path in settings.DATA_LIST:
        path_string, cls_name = path.rsplit('.', maxsplit=1)

        m = importlib.import_module(path_string)
        cls = getattr(m, cls_name)
        obj = cls(123)
        # print(obj)
        # obj.handler()
        if not hasattr(obj, 'handler'):
            continue
        method = getattr(obj, 'handler')
        method()


if __name__ == '__main__':
    run()
