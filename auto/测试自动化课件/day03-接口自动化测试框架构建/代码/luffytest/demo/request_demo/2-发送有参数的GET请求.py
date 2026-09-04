import requests

params = {
    'name': 'moluo',
    'age': 18
}
response = requests.get("http://httpbin.org/get?sex=1", params=params)
print(response.text)
