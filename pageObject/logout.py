#Author: ls Liu
'''
封装登出功能
'''
from Common.CommonFunc import WebTools

class logout():
    def __init__(self,driver):
        self.driver = driver

    def logout(self):
        WebTools(self.driver).mouser_move_action('xpath',"//a[@data-toggle='dropdown']")
        WebTools(self.driver).mouse_click('xpath',"//a[contains(text(),'修改密码')]/../..//a[contains(text(),'注销')]")
        #WebTools(self.driver).mouser_move_action('xpath',"//a[contains(text(),'修改密码')]/../..//a[contains(text(),'注销')]")
