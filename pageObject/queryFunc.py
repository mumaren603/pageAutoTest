'封装流程中查询功能'
import time
from Common.ToolsForOpertion import WebTools
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from Common.LogFunc import loggerConf

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
                :param ywlxID: 业务类型ID
            :param params (dict)
                :param cqType :产权类型（0-净地，1-房屋）
        :return:
        '''
        qllx = data.get('initdata').get('lcInfo',None).get('qllx',None)
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)

        # 查封业务
        if qllx == '查封登记':
            # # 批量查封（净地需要切换处理）,因接口合并，没有关联业务类型ID，所以需要加上净地判断
            # if ywlxID == '80E93B91E9974F98AAE75C6AD28629B1':
            #     if cqType == 0:
            #         WebTools(self.driver).mouse_click('xpath', "//span[@xid='landBtn']")
            #         WebTools(self.driver).check_element_is_exists('xpath',"//input[@xid='zddm']/../../..//input[@xid='bdcdyh']")
            #         WebTools(self.driver).input_content('xpath', "//input[@xid='zddm']/../../..//input[@xid='bdcdyh']",bdcdyh)
            #         WebTools(self.driver).mouse_click('xpath',"//input[@xid='zddm']/../../..//span[contains(text(),'查询')]")
            #         time.sleep(2)
            #         WebTools(self.driver).check_element_is_exists('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
            #         WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
            #         WebTools(self.driver).mouse_click('xpath', "//input[@xid='zddm']/../../../../../../..//*[@id='confirmBtn']")
            # # 批量预售合同查封
            # elif ywlxID == '7C472DAB0C1D46E1B782689C057B552E':
            #     WebTools(self.driver).mouse_click('xpath', "//span[@xid='landBtn']")
            #     WebTools(self.driver).check_element_is_exists('xpath',"//span[@xid='landBtn']/../../div[3]/div[2]//*[@xid='bdcdyh']")
            #     WebTools(self.driver).input_content('xpath',"//span[@xid='landBtn']/../../div[3]/div[2]//*[@xid='bdcdyh']",bdcdyh)
            #     WebTools(self.driver).mouse_click('xpath', "//span[@xid='landBtn']/../../div[3]/div[2]//span[contains(text(),'查询')]")
            #     time.sleep(2)
            #     WebTools(self.driver).check_element_is_exists('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
            #     WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
            #     WebTools(self.driver).mouse_click('xpath',"//input[@xid='zddm']/../../../../../../..//*[@id='confirmBtn']")
            # # 批量司法裁定/预告司法裁定（净地需要切换处理）
            # elif ywlxID == 'EF4D6596ED6347DDA33471FCFA7E973A' or ywlxID == 'EB661D9603EF48E895503BDBC82EADAA':
            #     WebTools(self.driver).mouse_click('xpath', "//span[@xid='landBtn']")
            #     WebTools(self.driver).check_element_is_exists('xpath',"//input[@xid='zdtybm']/../../..//input[@xid='bdcdyh']")
            #     WebTools(self.driver).input_content('xpath', "//input[@xid='zdtybm']/../../..//input[@xid='bdcdyh']", bdcdyh)
            #     WebTools(self.driver).mouse_click('xpath', "//input[@xid='zdtybm']/../../..//span[contains(text(),'查询')]")
            #     time.sleep(2)
            #     WebTools(self.driver).check_element_is_exists('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
            #     WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
            #     WebTools(self.driver).mouse_click('xpath', "//input[@xid='zdtybm']/../../../../../../..//*[@id='confirmBtn']")
            # 部分流程里区分房地和净地流程，净地流程需要切换净地查询页面，房地流程默认走通用模板


            # 批量司法裁定(净地)/预告司法裁定(净地)/批量查封(净地)
            '''因批量查封净地和房屋为一个接口，同一个ywlxid,只能加上产权类型判断'''
            if ywlxID == 'EF4D6596ED6347DDA33471FCFA7E973A' or ywlxID == 'EB661D9603EF48E895503BDBC82EADAA' or (ywlxID =='80E93B91E9974F98AAE75C6AD28629B1' and cqType == 0):
                WebTools(self.driver).mouse_click('xpath', "//span[@xid='landBtn']")
                WebTools(self.driver).check_element_is_exists('xpath', "//th[contains(text(),'宗地')]/../../..//input[@xid='bdcdyh']")
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'宗地')]/../../..//input[@xid='bdcdyh']",bdcdyh)
                WebTools(self.driver).mouse_click('xpath',"//th[contains(text(),'宗地')]/../../..//span[contains(text(),'查询')]")
                time.sleep(2)
                WebTools(self.driver).check_element_is_exists('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
                WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
                WebTools(self.driver).mouse_click('xpath', "//th[contains(text(),'宗地')]/../../../../../../..//*[@id='confirmBtn']")
            # 批量预售合同查封
            elif ywlxID == '7C472DAB0C1D46E1B782689C057B552E':
                WebTools(self.driver).mouse_click('xpath', "//span[@xid='landBtn']")
                WebTools(self.driver).check_element_is_exists('xpath',"//span[@xid='landBtn']/../../div[3]/div[2]//*[@xid='bdcdyh']")
                WebTools(self.driver).input_content('xpath',"//span[@xid='landBtn']/../../div[3]/div[2]//*[@xid='bdcdyh']",bdcdyh)
                WebTools(self.driver).mouse_click('xpath', "//span[@xid='landBtn']/../../div[3]/div[2]//span[contains(text(),'查询')]")
                time.sleep(2)
                WebTools(self.driver).check_element_is_exists('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
                WebTools(self.driver).mouse_click('xpath', "//table[@xid='resultTable']//tbody/tr[1]")
                WebTools(self.driver).mouse_click('xpath',"//span[@xid='landBtn']/../../div[3]/div[2]//span[contains(text(),'确认')]")
            # 通用模板（包括单个流程查询 和批量非净地流程查询）
            else:
                WebTools(self.driver).check_element_is_exists('xpath', "//input[@xid='bdcdyh']")
                WebTools(self.driver).input_content('xpath', "//input[@xid='bdcdyh']", bdcdyh)
                WebTools(self.driver).mouse_click('xpath', "//div[@xid='mainContent']//span[contains(text(),'查询')]")
                time.sleep(2)
                WebTools(self.driver).mouse_click('xpath',"//tbody[@xid='listTemplate1']//*[contains(text(),bdcdyh)]")
                # 滚动条拖到确认位置
                self.driver.execute_script("document.documentElement.scrollTop=300")
                WebTools(self.driver).mouse_click('id', "confirmBtn")

        # 非查封业务
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


