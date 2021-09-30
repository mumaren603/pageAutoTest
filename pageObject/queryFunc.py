'封装流程中查询功能'
import time
from Common.CommonFunc import WebTools
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from Common.logFunc import loggerConf

logger = loggerConf().getLogger()

class queryFunc():
    def __init__(self,driver):
        self.driver = driver

    def query(self,bdcdyh,data):
        '''
        流程发起菜单，包括一级菜单、二级菜单、三级菜单
        :param bdcdyh 受理件不动产单元号
        :param data (dict)
            :param lcInfo (dict)
                :param qllx: 权利类型,
                :param djlx: 登记类型（optional）
                :param ywlxID: 业务类型ID
            :param params (dict)
                :param cqType :产权类型（0-净地，1-房屋）
        :return:
        '''
        qllx = data.get('initdata').get('lcInfo',None).get('qllx',None)
        djlx = data.get('initdata').get('lcInfo', None).get('djlx', None)
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)

        if qllx =='查封登记':
            # 查封登记(房和地)/续查封登记（房和地）/司法裁定（房和地）/解封登记（房和地）
            if ywlxID == '6DFC6A6D5D214896AB5216424A8E02BE' or ywlxID == '87F9D867EFD04220805987CC776A7A9F' or ywlxID=='4F8E285959114451A95C5CFC31FD9E0F' or ywlxID=='AD8169CA47E844F6B240D36799F2AA06' or ywlxID =='4858445B1488454F970428A2436F54D5' or ywlxID =='8FEAF5CC34DF49C88B7E3139F8C0B18A' or ywlxID=='FB265E54DBE24577B2FA4F4C4980AB15' or ywlxID == '08B3B1B8F1FD47188C115939E2814AFF':
                if cqType == 0:
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='landBtn']")
                    WebTools(self.driver).check_element_is_exists('xpath', "//input[@xid='zdtybm']/../../..//input[@xid='bdcdyh']")
                    WebTools(self.driver).input_content('xpath', "//input[@xid='zdtybm']/../../..//input[@xid='bdcdyh']", bdcdyh)
                    WebTools(self.driver).mouse_click('xpath', "//input[@xid='zdtybm']/../../..//span[contains(text(),'查询')]")
                    time.sleep(2)
                    WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
                    WebTools(self.driver).mouse_click('xpath', "//input[@xid='zdtybm']/../../../../../../..//*[@id='confirmBtn']")
                elif cqType == 1:
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='houseBtn']")
                    WebTools(self.driver).check_element_is_exists('xpath', "//input[@xid='fwdm']/../../..//input[@xid='bdcdyh']")
                    WebTools(self.driver).input_content('xpath', "//input[@xid='fwdm']/../../..//input[@xid='bdcdyh']", bdcdyh)
                    WebTools(self.driver).mouse_click('xpath', "//input[@xid='fwdm']/../../..//span[contains(text(),'查询')]")
                    time.sleep(2)
                    WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
                    WebTools(self.driver).mouse_click('xpath', "//input[@xid='fwdm']/../../../../../../..//*[@id='confirmBtn']")
                else:
                    logger.error("入参%s定义错误" % cqType)
            else:
                WebTools(self.driver).check_element_is_exists('xpath', "//input[@xid='bdcdyh']")
                WebTools(self.driver).input_content('xpath', "//input[@xid='bdcdyh']", bdcdyh)
                WebTools(self.driver).mouse_click('xpath', "//div[@xid='mainContent']//span[contains(text(),'查询')]")
                time.sleep(2)
                try:
                    WebTools(self.driver).mouse_click('xpath',"//tbody[@xid='listTemplate1']//*[contains(text(),bdcdyh)]")
                except:
                    pass
                WebTools(self.driver).mouse_click('id',"confirmBtn")
        else:
            # 建筑物区分业主共有部分（通过幢不动产单元号查询）
            if ywlxID == '191B4FB37DD148448BC64944C01A78C1':
                WebTools(self.driver).check_element_is_exists('xpath', "//input[@xid='zbdcdyh']")
                WebTools(self.driver).input_content('xpath', "//input[@xid='zbdcdyh']", bdcdyh)
            else:
                WebTools(self.driver).check_element_is_exists('xpath', "//input[@xid='bdcdyh']")
                WebTools(self.driver).input_content('xpath', "//input[@xid='bdcdyh']", bdcdyh)
            WebTools(self.driver).mouse_click('xpath', "//div[@xid='mainContent']//span[contains(text(),'查询')]")
            time.sleep(2)
            WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
            # WebTools(self.driver).mouse_click('id', "confirmBtn")
            # 分户转移
            if ywlxID == 'CD62B1699DEB4496AF8D5D5590E945AB':
                WebTools(self.driver).mouse_click('xpath',"//div[@xid='confirm']")
            else:
                WebTools(self.driver).mouse_click('xpath',"//span[contains(text(),'确认')]")
        # 针对页面点击确定弹出框提示信息，点击确定
        WebTools(self.driver).allow_element_is_exists('class_name', 'BeAlert_box')

    # 针对批量业务不动产基本信息页面新增单元查询
    def bdcjbxxQuery(self,bdcdyh,data):
            ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
            # 项目类多幢首次
            if ywlxID == '608286609F5C429CB32BA42C56F7C7F7':
                WebTools(self.driver).check_element_is_exists('xpath', "//div[@xid='_compose_xzdyDialog_']//input[@xid='bdcdyh']")
                WebTools(self.driver).input_content('xpath', "//div[@xid='_compose_xzdyDialog_']//input[@xid='bdcdyh']", bdcdyh)
                WebTools(self.driver).mouse_click('xpath', "//div[@xid='_compose_xzdyDialog_']//span[contains(text(),'查询')]")
                time.sleep(2)
                WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]//td[contains(text(),'"+bdcdyh+"')]")
                WebTools(self.driver).mouse_click('xpath',"//div[@xid='_compose_xzdyDialog_']//span[contains(text(),'确认')]")
                # 针对页面点击确定弹出框提示信息，点击确定
                WebTools(self.driver).allow_element_is_exists('class_name', 'BeAlert_box')


