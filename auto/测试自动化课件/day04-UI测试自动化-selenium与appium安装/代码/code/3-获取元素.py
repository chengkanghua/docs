import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# 打开一个页面
driver.get("https://www.luffycity.com")

# 基于xpath路径获取元素
element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/img[1]')

# # 基于css选择符获取元素
# element = driver.find_element(By.CSS_SELECTOR, '#__layout > div > div.mbox > div > img.close')

# # 基于class属性值来获取元素
# element = driver.find_elements(By.CLASS_NAME, 'close')
# # 如果使用find_elements获取多个元素，返回结果是一个列表，需要通过下标来选择操作的是哪一个？
# element = element[0]


# 等待3秒以后点击(这个等待不是必须的，而是为了方便查看而已)
time.sleep(3)
print(element.click())

# 等待10秒退出，如果当前窗口只有一个浏览器页面，则表示退出当前浏览器
time.sleep(10)
driver.close()
