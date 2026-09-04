import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 规避网站监测
option.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'}) # 规避网站监测

# 打开一个页面
driver.get("https://mail.163.com")

iframe_list = driver.find_elements(By.TAG_NAME, 'iframe')
form_iframe = iframe_list[0]
# 切换窗口到指定iframe
driver.switch_to.frame(form_iframe)

driver.find_element(By.NAME, 'email').send_keys('moooluo2022')
# time.sleep(3)
# driver.find_element(By.NAME, 'email').clear()

driver.find_element(By.NAME, 'password').send_keys('123456')

driver.find_element(By.ID, 'dologin').click()

# 等待10秒退出，如果当前窗口只有一个浏览器页面，则表示退出当前浏览器
time.sleep(10)
driver.close()
