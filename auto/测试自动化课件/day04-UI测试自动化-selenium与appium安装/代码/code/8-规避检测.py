import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 规避网站监测
option.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'}) # 规避网站监测


driver.get("https://www.baidu.com")

driver.find_element(By.ID, "kw").send_keys("路飞学城")
driver.find_element(By.ID, "su").click()

time.sleep(5)
driver.quit()
