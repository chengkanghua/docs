import requests

data = {'name': 'moluo', 'age': '22'}
response = requests.post("http://httpbin.org/post", json=data)
print(response.text)
