import pytest,os
from utils.getTestdataForJson import getTestcaseData,getTestdataPath
from Common.ToolsForOpertion import WebTools
from init.dataInit import dataInit
from pageObject.logout import logout
from Common.LogFunc import loggerConf
logger = loggerConf().getLogger()

@pytest.mark.all
class Test_houseCqQuery():
    def setup_class(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))
        print("测试数据：",self.data)

    # 输入正确查询条件，查询结果正确，正常出产调证明
    def test_1(self,openQueryCenter):
        global driver
        driver = openQueryCenter[0]
        bdcdyh = dataInit().getHouseCqRegisterData()
        WebTools(driver).mouse_click('xpath',"//th[contains(text(),'查询条件')]/..//label[2]/span[1]")
        WebTools(driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",bdcdyh)
        # WebTools(driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",'321322100002GB00124F50210105')
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")
        # WebTools(driver).mouse_click('xpath',"//span[contains(text(),'321322100002GB00124F50210105')]/../../../td[1]//input[@type='checkbox']")
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'"+ bdcdyh +"')]/../../../td[1]//input[@type='checkbox']")
        WebTools(driver).mouse_click('xpath',"//span[(text()='现势信息')]/..//span[contains(text(),'登记证明')]")
        import time
        time.sleep(2)

        val= WebTools(driver).is_element_exist("//*[@id='viewer']")
        assert val
        # WebTools(driver).switch_back_iframe()
        # WebTools(driver).mouse_click('xpath',"//a[@xid='closeFuncBtn']")

    def test_4(self):
        print("执行测试用例4啦。。。")
        # WebTools(self.driver).mouse_click('xpath',"//span[contains(text(),'返回')]")
        WebTools(driver).mouse_click('xpath',"//th[contains(text(),'查询条件')]/..//label[2]/span[1]")
        WebTools(driver).input_clear('xpath',"//label[contains(text(),'不动产单元号')]/..//input")
        WebTools(driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",'12312312312')
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")

        WebTools(driver).switch_back_iframe()

    def teardown_class(self):
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        # 退出系统
        logout(driver).logout()
        # 退出浏览器
        driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'Test_houseCqQuery'])
