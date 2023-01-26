"""
目录查看器
- 提示用户输入要查看的目录。
- 监测目录是否存在。 不存在，则提示目录不存在；存在，则展示目录下所有的文件和文件夹。
"""
# import os
#
# while True:
#     folder = input("请输入目录名称：")
#     if not os.path.exists(folder):
#         print("目录不存在")
#         continue
#
#     for item in os.listdir(folder):
#         print(item)


# import os
#
# folder_list = []
#
# while True:
#     if not folder_list:
#         print("未选择路径")
#     else:
#         current_path = "/".join(folder_list)
#         print(current_path)
#
#     folder = input("请输入目录名称：")
#     # 1.输入B终止
#     if folder.upper() == "B":
#         break
#
#     # 2.输入Q，返回上一节路径    []     ["xx"]    ['xx','x1']
#     if folder.upper() == "Q":
#         # 判断是否是 []
#         if not folder_list:
#             print("目前未进入任何路径，无法返回上一节")
#             break
#         # [x1]    ['xx']
#         folder_list.pop()
#         if not folder_list:
#             print("已返回至初始目录")
#             continue
#         target_folder = os.path.join(*folder_list)
#     else:
#         target_folder = os.path.join(*folder_list, folder)
#
#     if not os.path.exists(target_folder):
#         print("目录不存在")
#         continue
#
#     if not os.path.isdir(target_folder):
#         print('不是文件夹')
#         continue
#
#     if folder.upper() != "Q":
#         folder_list.append(folder)
#
#     for item in os.listdir(target_folder):
#         print(item)


# data = {
#     "河北":{
#         "廊坊":{}
#     }
# }
