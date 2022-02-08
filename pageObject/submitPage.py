import time
from Common.ToolsForOpertion import WebTools
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class submitPage():
    def __init__(self,driver):
        self.driver = driver

    def slHandle(self):
        '''
        :param link: 受理环节
        :return:
        '''
        # 提交
        WebTools(self.driver).mouse_click('xpath', '//span[@functionname="commitBtnClick"]')
        # 受理环节弹出框确定按钮
        WebTools(self.driver).check_element_is_exists('xpath', "//a[@xid='okBtn']")
        time.sleep(1)
        WebTools(self.driver).mouse_click('xpath', "//a[@xid='okBtn']")
        WebTools(self.driver).check_element_is_exists('xpath','//span[@xid="newTask"]')

    def shHandle(self,bdcdyh):
        '''
        :param bdcdyh: 不动产单元号
        :return:
        '''
        # 办件中心检索该办件业务
        self.driver.execute_script('document.documentElement.scrollTop=document.body.clientHeight')
        WebTools(self.driver).mouse_click('xpath',"//select[@xid='mySelect']//option[@value='BDCDYH']")
        WebTools(self.driver).input_clear('xpath',"//input[@xid='myText']")
        WebTools(self.driver).input_content('xpath',"//input[@xid='myText']",bdcdyh)
        WebTools(self.driver).mouse_click('xpath',"//span[@xid='search']")

        # 校验该数据是否存在
        WebTools(self.driver).check_element_is_exists('xpath',"//div[contains(text(),'初审') or contains(text(),'复审')]/../..")
        WebTools(self.driver).mouse_doubleClick('xpath',"//div[contains(text(),'初审') or contains(text(),'复审')]/../..")

        # 填写复审/审核意见
        WebTools(self.driver).check_element_is_exists('xpath',"//textarea[@xid='currentShyj']")
        WebTools(self.driver).input_content('xpath', "//textarea[@xid='currentShyj']", '同意')

        # 提交
        WebTools(self.driver).mouse_click('xpath', '//span[@functionname="commitBtnClick"]')
        WebTools(self.driver).check_element_is_exists('xpath', "//a[@xid='okBtn']")
        WebTools(self.driver).mouse_click('xpath', "//a[@xid='okBtn']")
        WebTools(self.driver).check_element_is_exists('xpath', '//span[@xid="newTask"]')

    def dbHandle(self,bdcdyh,data):
        '''
        登簿环节
        :bdcdyh: 不动产单元号
        :return:
        '''
        # 办件中心检索该办件业务是否存在
        self.driver.execute_script('document.documentElement.scrollTop=document.body.clientHeight')
        WebTools(self.driver).mouse_click('xpath',"//select[@xid='mySelect']//option[@value='BDCDYH']")
        WebTools(self.driver).input_clear('xpath',"//input[@xid='myText']")
        WebTools(self.driver).input_content('xpath',"//input[@xid='myText']",bdcdyh)
        WebTools(self.driver).mouse_click('xpath',"//span[@xid='search']")

        # 校验该数据是否存在
        # WebTools(self.driver).check_element_is_exists('xpath',"//div[contains(text(),'"+bdcdyh+"')]/../..")
        # WebTools(self.driver).mouse_doubleClick('xpath',"//div[contains(text(),'"+bdcdyh+"')]/../..")
        WebTools(self.driver).check_element_is_exists('xpath',"//div[contains(text(),'登簿')]/../..")
        WebTools(self.driver).mouse_doubleClick('xpath',"//div[contains(text(),'登簿')]/../..")

        # 登簿意见
        WebTools(self.driver).check_element_is_exists('xpath',"//textarea[@xid='shyj0']")
        WebTools(self.driver).check_element_is_exists('xpath',"//textarea[@xid='currentShyj']")
        WebTools(self.driver).input_content('xpath',"//textarea[@xid='currentShyj']",'审核同意')

        # # 登簿
        # WebTools(self.driver).mouse_click('link_text', '登簿')
        # WebTools(self.driver).check_element_is_exists('xpath',"//input[@xid='YWH']")

        # 登簿提交
        WebTools(self.driver).mouse_click('xpath','//span[@functionname="commitBtnClick"]')
        #任务流转==>制证(非注销流程)
        WebTools(self.driver).check_element_is_exists('xpath',"//a[@xid='okBtn']")
        WebTools(self.driver).mouse_click('xpath', "//a[@xid='okBtn']")
        WebTools(self.driver).check_element_is_exists('xpath','//span[@xid="myTask"]')





