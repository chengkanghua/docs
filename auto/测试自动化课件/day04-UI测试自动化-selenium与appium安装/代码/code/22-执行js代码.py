import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.luffycity.com")

# 关闭广告
element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/img[1]')
element.click()

num = 0
while num <= driver.execute_script("""return parseInt(getComputedStyle(document.querySelector('.main'))["height"])"""):
    num += 1
    driver.execute_script(f"window.scrollTo(0, {20*num})")
    time.sleep(0.01)

time.sleep(3)
driver.quit()

