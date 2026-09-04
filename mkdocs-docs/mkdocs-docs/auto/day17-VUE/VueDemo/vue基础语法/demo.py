import requests



res = requests.get("https://2019ncov.chinacdc.cn/JKZX/yq_20220401.json")


print(res.json())