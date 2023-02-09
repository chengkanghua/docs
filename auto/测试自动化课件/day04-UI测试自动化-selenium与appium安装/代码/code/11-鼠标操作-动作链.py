import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

service = Service("chromedriver.exe")
driver=webdriver.Chrome(service=service)

# 打开一个网址
driver.get("C:/Users/Administrator/Desktop/code/11-测试页面.html")

element = driver.find_element(By.CLASS_NAME, 'box')
ActionChains(driver).move_to_element(element).perform()
time.sleep(1)
ActionChains(driver).double_click().perform()
time.sleep(3)
driver.quit()