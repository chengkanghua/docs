import requests

params = {
    'name': 'moluo',
    'age': 18
}
response = requests.get("http://httpbin.org/get", params=params)
print(response.content)
print(response.text)