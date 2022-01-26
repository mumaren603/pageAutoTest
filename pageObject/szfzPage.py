import time
from Common.ToolsForOpertion import WebTools

class szfzPage():
    def __init__(self,driver):
        self.driver = driver

    # 缮证
    def szHandle(self,bdcdyh,env):
        # 将页面滚动条拖到顶部
        self.driver.execute_script("var q = document.documentElement.scrollTop=0")

        WebTools(self.driver).mouse_doubleClick('xpath',"//div[contains(text(),'"+bdcdyh+"')]/../..")
        WebTools(self.driver).check_element_is_exists('xpath','//span[@xid="saveZsZmBtn"]')
        # time.sleep(1)

        #提交
        if env == 'sqtest':
            WebTools(self.driver).mouse_click('xpath','//span[@functionname="commitBtnClick"]')
        else:
            WebTools(self.driver).mouse_click('xpath','//div[@id="applicationHost"]/div[1]/div[2]/div/section[2]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/span[1]')
        WebTools(self.driver).check_element_is_exists('class_name','BeAlert_box')
        WebTools(self.driver).mouse_click('xpath','//button[@class="BeAlert_confirm"]')
        time.sleep(1)

        # 任务流转==>发证
        WebTools(self.driver).check_element_is_exists('xpath', "//span[@xid='span31_1']")
        WebTools(self.driver).mouse_click('xpath', "//span[@xid='span31_1']")

    # 发证
    def fzHandle(self,bdcdyh,env):
        # 将页面滚动条拖到顶部
        self.driver.execute_script("var q = document.documentElement.scrollTop=0")

        WebTools(self.driver).mouse_doubleClick('xpath', "//div[contains(text(),'" + bdcdyh + "')]/../..")
        WebTools(self.driver).check_element_is_exists('xpath','//span[@xid="editBtn"]')
        # time.sleep(2)

        if env =='sqtest':
            WebTools(self.driver).mouse_click('xpath', '//span[@functionname="commitBtnClick"]')
        else:
            WebTools(self.driver).mouse_click('xpath','//span[@xid="editBtn"]')
            WebTools(self.driver).choose_droplist_value('rylx','xpath','//select[@name="rylx"]/option[2]')
            WebTools(self.driver).input_content('xpath','//input[@xid="FZSL"]',1)
            WebTools(self.driver).choose_droplist_value('lzrzjlb','xpath','//select[@name="lzrzjlb"]/option[4]')
            WebTools(self.driver).input_content('xpath','//input[@xid="LZRZJHM"]',121212)
            WebTools(self.driver).choose_droplist_value('lzfs','xpath','//select[@name="lzfs"]/option[2]')
            WebTools(self.driver).mouse_click('xpath','//span[@xid="saveBtn"]')
            WebTools(self.driver).mouse_click('xpath', '//span[@functionname="commitBtnClick"]')
            WebTools(self.driver).mouse_click('xpath','//div[@id="applicationHost"]/div[1]/div[2]/div/section[2]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/span[2]')

        # 任务流转==>结束
        WebTools(self.driver).mouse_click('xpath', "//a[@xid='okBtn']")




