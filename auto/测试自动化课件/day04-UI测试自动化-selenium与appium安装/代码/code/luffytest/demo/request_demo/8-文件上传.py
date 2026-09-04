import requests

# 支持上传一张或多张图片
files = {'avatar': open('1.png', 'rb')}
response = requests.post("http://httpbin.org/post", files=files)
print(response.text)