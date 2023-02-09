import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
service = Service("chromedriver.exe")
driver=webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})

driver.get("http://www.baidu.com")

driver.find_element(By.ID, "kw").send_keys("路飞学城")
driver.find_element(By.ID, "su").click()
# 使用time.sleep这种机械化的强制等待，实际上是有可能出问题的。即便没有问题，也会存在着让测试代码浪费等待时间的情况。
# time.sleep(3)
driver.find_element(By.PARTIAL_LINK_TEXT, "路飞学城").click()
# time.sleep(3)
# driver.quit()
