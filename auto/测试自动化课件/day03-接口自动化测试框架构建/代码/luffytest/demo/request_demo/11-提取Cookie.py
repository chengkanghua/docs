import requests

r = requests.get('https://www.baidu.com')
print(r.cookies)
print(r.cookies['BDORZ'])
print(tuple(r.cookies))