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

