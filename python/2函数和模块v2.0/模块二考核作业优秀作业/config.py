# 导入模块
import os

# 处理文件路径
file_video =os.path.dirname(os.path.abspath(__file__))
video_file_path = os.path.join(file_video,"db","video.csv")
print(file_video)