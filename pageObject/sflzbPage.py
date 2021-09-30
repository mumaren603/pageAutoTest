#封装流程受理（收费领证表）
'''
:param driver  浏览器驱动
'''
import time
from Common.CommonFunc import WebTools

class sflzbPage():
    def __init__(self,driver):
        self.driver = driver

    def sflzbHandle(self):
        WebTools(self.driver).check_element_is_exists('link_text','收费领证表')
        WebTools(self.driver).mouse_click('link_text', '收费领证表')
        self.driver.execute_script('document.documentElement.scrollTop=0')
        time.sleep(3)
        # WebTools(self.driver).check_element_is_exists('xpath','//span[@xid="initChargeBtn"]')
        # 收费信息
        WebTools(self.driver).mouse_click('xpath', "//span[@xid='initChargeBtn']")
        WebTools(self.driver).mouse_click('xpath',"//span[contains(text(),'收费完成')]")
        time.sleep(2)

        # 证书生成
        WebTools(self.driver).mouse_click('xpath', "//span[@xid='create']")
        time.sleep(3)








