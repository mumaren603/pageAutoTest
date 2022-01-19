# -*- coding: utf -8 -*-
#封装注销登记公共页面

import time
from Common.CommFunc import WebTools
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class cancleRegisterCommonPage():
    def __init__(self,driver):
        self.driver = driver

    def sjdHandle(self):
        WebTools(self.driver).mouse_click('link_text','收件单')
        WebTools(self.driver).check_element_is_exists('xpath','//input[@xid="YWLXMC"]')

    def sqrqkHandle(self,lcInfo):
        qllx = lcInfo.get('qllx',None)

        WebTools(self.driver).mouse_click('link_text', '申请人情况')
        if qllx == '抵押权':
            WebTools(self.driver).check_element_is_exists('xpath',"//table[@xid='upperTable']/thead//*[contains(text(),'抵押人列表')]")
        elif qllx == '国有建设用地使用权' or qllx == '国有建设用地使用权及房屋所有权':
            WebTools(self.driver).check_element_is_exists('xpath',"//table[@xid='underTable']/thead//*[contains(text(),'申请人信息')]")

    def sqbHandle(self):
        WebTools(self.driver).mouse_click('link_text', '申请表')
        WebTools(self.driver).check_element_is_exists('xpath','//input[@xid="qllxmc"]')

    def bdcjbxxHandle(self):
        WebTools(self.driver).mouse_click('link_text', '不动产基本信息')
        WebTools(self.driver).check_element_is_exists('xpath','//span[contains(text(),"不动产信息")]')

    def blyjHandle(self):
        WebTools(self.driver).mouse_click('link_text', '办理意见')
        WebTools(self.driver).input_content('xpath', "//textarea[@xid='currentShyj']", '同意')

    def xwjlHandle(self):
        WebTools(self.driver).mouse_click('link_text', '询问记录')
        WebTools(self.driver).input_content('xpath', "//textarea[@xid='currentShyj']", '同意')

    def dbHandle(self):
        WebTools(self.driver).mouse_click('link_text', '登簿')
        WebTools(self.driver).check_element_is_exists('xpath', '//table[@xid="printTable"]//*[contains(text(),"询问记录")]')
        #登簿提交
        WebTools(self.driver).mouse_click('xpath',"//div[@id='applicationHost']/div[1]/div[2]/div/section[2]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/span[2]")
        #任务流转==>结束
        WebTools(self.driver).mouse_click('xpath',"//span[@xid='span31_1']")
        #等待跳转到办件中心
        WebTools(self.driver).check_element_is_exists('xpath',"//span[@xid='myTask']")




