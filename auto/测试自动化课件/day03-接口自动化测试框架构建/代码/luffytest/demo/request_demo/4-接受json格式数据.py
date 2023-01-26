import requests
import json

response = requests.get("http://httpbin.org/get")
# 方式I：
print(json.loads(response.text))
# 方式2：
print(response.json())