import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)
# 设置浏览器的宽高
driver.set_window_size(1555, 768)
# 获取浏览器的宽高
ret = driver.get_window_size()
print(ret) # {'width': 1555, 'height': 770}
driver.get("https://www.luffycity.com")
print(f"网页标题：{driver.title}")
print(f"当前地址：{driver.current_url}")
time.sleep(3)
# 刷新浏览器当前页面
driver.refresh()
time.sleep(3)
# 刷新浏览器当前页面
driver.refresh()
time.sleep(3)

# 在当前窗口打开一个新页面
driver.get("https://www.baidu.com")
time.sleep(3)
# 返回上一步访问的url地址，相当于返回路飞
driver.back()
time.sleep(3)
# 前进到下一步访问的url地址，相当于前进到百度
driver.forward()

# 等待10秒退出，如果当前窗口只有一个浏览器页面，则表示退出当前浏览器
time.sleep(10)
driver.close()
