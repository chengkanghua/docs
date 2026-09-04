import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service


# 初始化一个谷歌浏览器实例对象
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                       {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})

driver.get('https://www.luffycity.com')

# 关闭广告
element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/img[1]')
element.click()

# 点击登陆
driver.find_element(By.CLASS_NAME, 'signin').click()
time.sleep(3)

# 往账号输入框输入账号
element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[1]/div[1]/input')
element.send_keys("13928835901")

# 往密码输入框输入密码
element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[1]/div[2]/input')
element.send_keys("123")

element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/button')
element.click()

time.sleep(2)
element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div')
# 通过元素的 screenshot 方法直接保存图片
element.screenshot('./login_result.png')
time.sleep(3)
driver.quit()
