import re

text = "13999999993"
data = re.findall('^1[358]\d{9}$', text)
print(data)
