import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
service = Service("chromedriver.exe")
driver=webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})

# 1. 先创建一个显式等待对象
wait = WebDriverWait(driver=driver, timeout=60, poll_frequency=0.5, ignored_exceptions=None)

driver.get("http://www.baidu.com")

driver.find_element(By.ID, "kw").send_keys("路飞学城")
driver.find_element(By.ID, "su").click()
# 使用time.sleep这种机械化的强制等待，实际上是有可能出问题的。即便没有问题，也会存在着让测试代码浪费等待时间的情况。
# time.sleep(3)
# driver.find_element(By.PARTIAL_LINK_TEXT, "路飞学城").click()

# 2. 显式等待对象调用判断等待方法
wait.until(expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, '路飞学城'))).click()

time.sleep(3)
driver.quit()
