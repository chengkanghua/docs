import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 规避网站监测
option.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告
service = Service("chromedriver.exe")
driver=webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'}) # 规避网站监测

# 打开一个页面
driver.get("https://www.baidu.com")

# 基于xpath路径获取元素
element = driver.find_element(By.ID, 'kw')
# 往输入框元素中通过键盘录入数据使用 send_keys()
element.send_keys("路飞学城")

# 找到提交按钮并点击
element = driver.find_element(By.ID, 'su')
element.click()

time.sleep(3)
# 从搜索结果找到有路飞学城的链接内容，并点击
element = driver.find_element(By.LINK_TEXT, '路飞学城')
element.click()
"""
错误提示：
NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"路飞学城"}
异常，没有这样的一个元素：基于  {"method":"link text","selector":"路飞学城"} 查找不到元素（本地元素不可达）
原因是百度在用户搜索内容以后，采用了ajax进行异步刷新页面数据的，所以会导致selenium代码在元素时，百度服务器有可能没有返回数据结果，没有数据结果则没有该结果连接，因此报错
"""

# 等待10秒退出，如果当前窗口只有一个浏览器页面，则表示退出当前浏览器
time.sleep(10)
driver.close()
