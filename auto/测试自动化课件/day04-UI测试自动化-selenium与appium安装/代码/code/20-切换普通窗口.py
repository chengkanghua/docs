import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.support import expected_conditions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                       {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})

wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.baidu.com")

    driver.find_element(By.ID, "kw").send_keys("路飞学城")
    driver.find_element(By.ID, "su").click()
    wait.until(expected_conditions.presence_of_element_located((By.LINK_TEXT, '路飞学城'))).click()
    # 查看当前浏览器中打开的窗口列表
    print(driver.window_handles)
    time.sleep(3)
    # 根据数组下标索引切换窗口
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, '百度百科').click()
    print(driver.window_handles)  # 此时应该有3个窗口了
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1]) # 切换到路飞窗口
finally:
    time.sleep(3)
    driver.quit()
