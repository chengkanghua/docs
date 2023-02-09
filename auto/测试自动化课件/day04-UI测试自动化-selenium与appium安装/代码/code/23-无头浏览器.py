import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

option = ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])  # 规避网站监测
option.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告

# 开启浏览器的无头模式
option.add_argument('--headless')
option.add_argument('--disable-gpu')  # 允许在无GPU的环境下运行，可选
option.add_argument('--window-size=1920x1080')  # 建议设置

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=option)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'}) # 规避网站监测
# 设置隐式等待
driver.implicitly_wait(time_to_wait=10)  # 只需要一个等待超时时间参数

# 打开网页
driver.get("https://www.baidu.com")
# 搜索内容
driver.find_element(By.ID, "kw").send_keys("路飞学城")
driver.find_element(By.ID, "su").click()

# 点击搜索结果
driver.find_element(By.PARTIAL_LINK_TEXT, "路飞学城").click()

# 调用浏览器驱动对象的save_screenshot方法就可以实现截图
driver.save_screenshot('./baidu_search_result.png')  # 图片必须保存为 png 格式

driver.quit()
