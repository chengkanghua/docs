import os
import shutil

for base_path, folder_list, name_list in os.walk("/Users/wupeiqi/Documents/路飞工作/爬虫和APP逆向课程/mp4"):
    for name in name_list:
        ext = name.split('.')[-1]
        if ext != 'mp4':
            continue
        # day01 fullstack s4 数据类型.mp4ß
        # day01 数据类型.mp4ß
        # xxx/xxxx/xxxx/xxx/day01 fullstack s4 数据类型.mp4ß
        file_path = os.path.join(base_path, name)

        new_name = name.replace("fullstack s4 ", "")
        # xxx/xxxx/xxxx/xxx/day01 数据类型.mp4ß
        new_file_path = os.path.join(base_path, new_name)

        shutil.move(file_path, new_file_path)
