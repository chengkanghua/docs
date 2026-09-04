import requests

response = requests.get('http://httpbin.org/get')
print(response.content)  # 获取原生内容
print(response.text)   # 获取文本内容
