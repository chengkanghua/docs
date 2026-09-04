from logging.handlers import WatchedFileHandler

import time
import os
from stat import ST_DEV, ST_INO, ST_MTIME

f = open('xxx.log', mode='a', encoding='utf-8')

sres = os.fstat(f.fileno())
dev, ino = sres[ST_DEV], sres[ST_INO]

while True:
    # 删除文件之后，报错
    try:
        new_sres = os.stat("xxx.log")
    except FileNotFoundError:
        new_sres = None

    if not new_sres or new_sres[ST_DEV] != dev or new_sres[ST_INO] != ino:
        print("文件被修改了 或 删除了 ")
        f = open('xxx.log', mode='a', encoding='utf-8')
        sres = os.fstat(f.fileno())
        dev, ino = sres[ST_DEV], sres[ST_INO]

    f.write("123123\n")
    f.flush()
    time.sleep(1)
