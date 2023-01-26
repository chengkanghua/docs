import requests

body = {'name': 'moluo', 'age': '22'}
response = requests.post("http://httpbin.org/post", data=body)
print(response.text)
