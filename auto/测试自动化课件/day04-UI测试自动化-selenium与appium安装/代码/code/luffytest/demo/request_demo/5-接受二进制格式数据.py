import requests

response = requests.get("http://httpbin.org/image/png")
with open("1.png", "wb") as f:
    f.write(response.content)
