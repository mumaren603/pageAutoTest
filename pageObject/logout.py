#Author: ls Liu
'''
封装登出功能
'''
from Common.ToolsForOpertion import WebTools
import time

class logout():
    def __init__(self,driver):
        self.driver = driver

    def logout(self):
        time.sleep(1)
        WebTools(self.driver).mouser_move_action('xpath',"//a[@data-toggle='dropdown']")
        WebTools(self.driver).check_element_is_exists('xpath',"//a[@data-toggle='dropdown' and @aria-expanded='true']")
        WebTools(self.driver).mouse_click('xpath',"//a[contains(text(),'修改密码')]/../..//a[contains(text(),'注销')]")
        #WebTools(self.driver).mouser_move_action('xpath',"//a[contains(text(),'修改密码')]/../..//a[contains(text(),'注销')]")
