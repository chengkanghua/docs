import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
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

# 进入页面
driver.get('https://www.jq22.com/yanshi10850')

iframe = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframe)

element1 = driver.find_element(By.XPATH, '//*[@id="bar"]/li[1]')
element2 = driver.find_element(By.XPATH, '//*[@id="foo"]')
time.sleep(3)
ActionChains(driver).drag_and_drop(element1, element2).perform()

time.sleep(10)
driver.quit()