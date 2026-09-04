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
# 设置隐式等待
driver.implicitly_wait(time_to_wait=10)  # 只需要一个等待超时时间参数

driver.get("https://www.baidu.com")

driver.find_element(By.ID, "kw").send_keys("路飞学城")
driver.find_element(By.ID, "su").click()

driver.find_element(By.PARTIAL_LINK_TEXT, "路飞学城").click()

time.sleep(3)
driver.quit()
