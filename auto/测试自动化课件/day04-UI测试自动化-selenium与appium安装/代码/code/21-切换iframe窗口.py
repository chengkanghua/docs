import time
import getpass
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def get_driver():
    """获取浏览器驱动对象"""
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=option)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})
    # 设置隐式等待
    driver.implicitly_wait(10)
    return driver

def task(url, username, password, to, theme):
    """
    发送邮件
    :param url  打开站点地址
    :param username 登陆账号
    :param password 登陆密码
    :param to 收件人邮箱账号
    :param theme 邮件的主体
    """
    driver.get(url)
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe[0])
    driver.find_element(By.CLASS_NAME, 'dlemail').send_keys(username)
    driver.find_element(By.CLASS_NAME, 'dlpwd').send_keys(password)
    driver.find_element(By.ID, 'dologin').click()
    # 登陆以后刷新了页面了，所以需要重新获取driver浏览器驱动对象，否则无法进行后续操作
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element(By.ID, '_mail_component_149_149').click()
    driver.find_element(By.CLASS_NAME, 'nui-editableAddr-ipt').send_keys(to)
    driver.find_elements(By.CLASS_NAME, 'nui-ipt-input')[2].send_keys(theme)

    content_iframe = driver.find_element(By.CLASS_NAME, 'APP-editor-iframe')
    driver.switch_to.frame(content_iframe)
    driver.find_element(By.TAG_NAME, "p").send_keys("这是通过selenium添加的邮件内容！！！")
    driver.switch_to.default_content()
    # 发送邮件
    driver.find_elements(By.CLASS_NAME, 'nui-btn-text')[2].click()

if __name__ == '__main__':
    url = 'https://mail.163.com'
    theme = '一份测试邮件'
    to = '649641514@qq.com'
    content = '测试邮件内容.................................'
    # username = input('用户名: ').strip()
    username = "moooluo2022"
    # pycharm中直接运行python脚本会导致getpass进入阻塞，所以需要使用终端命令行运行python脚本
    password = getpass.getpass(prompt="密码: ")
    driver = get_driver()
    try:
        task(url, username, password, to, content)
    except Exception as e:
        print(f"发送邮件出错：{e}")
    finally:
        time.sleep(20)
        driver.quit()

