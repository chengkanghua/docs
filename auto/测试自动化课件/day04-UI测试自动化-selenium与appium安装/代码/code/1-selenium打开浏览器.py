import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# # 旧版本selenium指定webdriver.exe的路径，操作对应的浏览器
# driver = webdriver.Chrome(executable_path="./chromedriver.exe")
# print(driver)

# 旧版本selenium指定webdriver.exe的路径，初始化一个谷歌浏览器实例对象
service = Service(executable_path="./chromedriver.exe")

# driver浏览器驱动对象，是一个连接对象，提供了操作浏览器的具体的功能方法以及与浏览器相关的功能参数等等
driver = webdriver.Chrome(service=service)
print(driver)

# 浏览器最小化窗口
driver.minimize_window()

# 通过driver.get方法打开一个网址，相当于新建一个窗口
driver.get("https://www.luffycity.com")

time.sleep(5)

# 关闭浏览器
driver.quit()

