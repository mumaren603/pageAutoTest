import pytest,os
from utils.getTestdataForJson import getTestcaseData,getTestdataPath
from Common.ToolsForOpertion import WebTools
from pageObject.logout import logout
from Common.LogFunc import loggerConf
logger = loggerConf().getLogger()

@pytest.mark.all
class Test_query():
    def setup_class(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))
    # def setup(self):
    #     '''初始化用户数据获取'''
    #     current_file_path = os.path.abspath(__file__).replace('\\','/')
    #     self.data = getTestcaseData(getTestdataPath(current_file_path))

    def test_1(self,openQueryCenter):
        self.driver = openQueryCenter[0]
        dbInfo = openQueryCenter[1]
        print("执行测试用例1啦。。。")
        print("case1:", openQueryCenter)
        WebTools(self.driver).mouse_click('xpath',"//th[contains(text(),'查询条件')]/..//label[2]/span[1]")
        WebTools(self.driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",'321322100002GB00124F50210105')
        WebTools(self.driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(self.driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")

        WebTools(self.driver).switch_back_iframe()
        WebTools(self.driver).mouse_click('xpath',"//a[@xid='closeFuncBtn']")
        assert True

    def test_4(self,openQueryCenter):
        self.driver = openQueryCenter[0]
        print("执行测试用例4啦。。。")
        print("case4:", openQueryCenter)
        # WebTools(self.driver).mouse_click('xpath',"//span[contains(text(),'返回')]")
        WebTools(self.driver).mouse_click('xpath',"//th[contains(text(),'查询条件')]/..//label[2]/span[1]")
        WebTools(self.driver).input_clear('xpath',"//label[contains(text(),'不动产单元号')]/..//input")
        WebTools(self.driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",'12312312312')
        WebTools(self.driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(self.driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")

    def teardown_class(self):
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        # 退出系统
        logout(self.driver).logout()
        # 退出浏览器
        self.driver.quit()

    # def teardown(self):
    #     logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        # # 退出系统
        # logout(self.driver).logout()
        # # 退出浏览器
        # self.driver.quit()

# if __name__ == '__main__':
#     pytest.main(['-v', 'Test_query'])
