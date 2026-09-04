import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# 初始化一个谷歌浏览器实例对象
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

# 打开一个网址
driver.get("http://localhost:63342/code/7.html?_ijt=gom325r5bev2q5u5q3uelkchje")

# # 查看元素的显示模式，是否是可见
# element = driver.find_element(By.NAME, 'access_token')
# display = element.is_displayed()
# print(display)
#
# # 查看元素的属性值
# print(element.get_attribute("value"))
# outline = element.value_of_css_property('border')
# print(outline)

# element = driver.find_element(By.XPATH, '/html/body/form/input[4]')
# enabled = element.is_enabled()
# print(enabled)

# # 提交表单
# element = driver.find_element(By.XPATH, '/html/body/form/input[5]')
# element.submit()


element = driver.find_element(By.XPATH, '/html/body/h1')
print(element.text)

time.sleep(5)
driver.quit()
