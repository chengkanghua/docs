import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# 初始化一个谷歌浏览器实例对象
option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
service = Service("chromedriver.exe")
driver=webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})


# 打开一个网址
driver.get("https://www.luffycity.com")

# 关闭广告
element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/img[1]')
element.click()

time.sleep(5)

element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div/div/nav/a[6]')
# move_to_element 把鼠标悬停在指定元素上面
# context_click 执行鼠标右键
# 动作链在设置动作以后，不会自动执行，所以需要在动作链的末尾，调用perform执行整个动作链
ActionChains(driver).move_to_element(element).context_click().perform()

time.sleep(5)
driver.quit()
