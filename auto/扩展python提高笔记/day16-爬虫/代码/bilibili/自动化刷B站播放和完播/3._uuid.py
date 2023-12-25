import time
import uuid


def gen_uuid():
    uid = str(uuid.uuid4())

    div = str(int(int(time.time() * 1000) % 1e5))
    div = div.ljust(5, "0")

    return "{}{}{}".format(uid, div, "infoc")


if __name__ == '__main__':
    _uuid = gen_uuid()
    print(_uuid)
