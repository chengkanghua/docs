# f1 = open("stock.csv", mode='r', encoding='utf-8')
# f1.readline()
#
# for line in f1:
#     line = line.strip()
#     row_list = line.split(',')
#     print(row_list)
#
# f1.close()

import os

BASE_DIR = "log"

for name in os.listdir(BASE_DIR):
    file_path = os.path.join(BASE_DIR, name)
    f = open(file_path, mode='r', encoding='utf-8')
    f.readline()
    for line in f:
        line = line.strip()
        print(line)
    f.close()
