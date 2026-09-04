import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_driver():
    # 初始化一个谷歌浏览器实例对象
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    return driver


def task(username, password):
    # 打开一个网址
    driver.get("https://www.luffycity.com")
    time.sleep(3)  # 可以不用，这句代码的作用主要是便于观察

    # 关闭广告
    driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/img[1]').click()

    # 点击登陆
    driver.find_element(By.CLASS_NAME, 'signin').click()
    time.sleep(3)

    # 往账号输入框输入账号
    element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[1]/div[1]/input')
    element.send_keys(username)

    # 往密码输入框输入密码
    element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[1]/div[2]/input')
    element.send_keys(password)

    element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/button')
    element.click()

    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    username = input("账号: ")
    # python的getpass会与pycharm内置的run终端形成阻塞，
    # 所以使用了getpass，则需要改成cmd或pycharm的Terminal终端来运行python脚本
    password = getpass("密码：")
    driver = get_driver()
    task(username, password)
