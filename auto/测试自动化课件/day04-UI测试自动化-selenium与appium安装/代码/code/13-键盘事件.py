import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
service = Service("chromedriver.exe")
driver=webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})

# 设置浏览器窗口最大化
driver.maximize_window()
# driver.minimize_window()  # 最小化
# 进入页面
driver.get('https://www.baidu.com/')
# 定位输入框
element = driver.find_element(By.ID, "kw")
# 向输入框中输入内容
element.send_keys("路飞学城")
time.sleep(2)
# 删除上一步中多输入的文字
element.send_keys(*[Keys.BACK_SPACE for i in range(2)])
element.send_keys("在线教育")

time.sleep(2)
# 使用回车代替点击按钮
element.send_keys(Keys.ENTER)
time.sleep(2)
