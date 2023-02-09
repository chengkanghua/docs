import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("C:/Users/Administrator/Desktop/code/12-测试页面.html")
time.sleep(3)
element = driver.find_element(By.TAG_NAME, "textarea")
element.send_keys(Keys.CONTROL, 'a')
element.send_keys(Keys.BACK_SPACE)

time.sleep(3)
element.send_keys("2012年9月25日，辽宁舰正式交付中国海军；2019年12月17日，山东舰入列，中国海军进入双航母时代；2022年6月17日，福建舰来了，我们有三艘航母了。")

time.sleep(5)
driver.quit()
