import requests
# https://www.beesproxy.com/free
proxies = {
    # "http": "http://112.6.117.135:8085",
    "http": "http://223.68.190.136:9091",
}
req = requests.get('http://icanhazip.com/', proxies=proxies)
print(req.text)
