import os

# 只罗列一级
# for item in os.listdir("xx"):
#     print(item)


for base_path, folder_list, name_list in os.walk("/Users/wupeiqi/Documents/路飞工作/爬虫和APP逆向课程/mp4"):
    for name in name_list:
        ext = name.split('.')[-1]
        if ext != 'mp4':
            continue
        file_path = os.path.join(base_path, name)
        print(file_path)
