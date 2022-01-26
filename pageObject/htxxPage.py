'''合同信息页面'''
from Common.ToolsForOpertion import WebTools
import time

class htxxPage():
    def __init__(self,driver):
        self.driver = driver

    # 房地产买卖合同
    def fdcmmhtHandle(self):
        WebTools(self.driver).check_element_is_exists('link_text','房地产买卖合同')
        WebTools(self.driver).mouse_click('link_text', '房地产买卖合同')
        WebTools(self.driver).check_element_is_exists('xpath','//div[@xid="sjsTit"]')

    # 抵押合同
    def dyhtHandle(self):
        WebTools(self.driver).check_element_is_exists('link_text','房地产抵押合同')
        WebTools(self.driver).mouse_click('link_text', '房地产抵押合同')
        WebTools(self.driver).check_element_is_exists('xpath','//div[@xid="sjsTit"]')

    # 询问记录
    def xwjlHandle(self):
        WebTools(self.driver).check_element_is_exists('link_text','询问记录')
        WebTools(self.driver).mouse_click('link_text', '询问记录')
        WebTools(self.driver).check_element_is_exists('xpath','//table[@xid="printTable"]//*[contains(text(),"询问记录")]')


