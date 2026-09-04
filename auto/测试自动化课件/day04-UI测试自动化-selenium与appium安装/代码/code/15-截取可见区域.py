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

# 调用浏览器驱动对象的save_screenshot方法就可以实现截图
driver.save_screenshot('./luffycity.png')  # 图片必须保存为 png 格式
driver.quit()
