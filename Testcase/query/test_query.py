import pytest,os
from utils.getTestdataForJson import getTestcaseData,getTestdataPath
from pageObject.taskCenter import taskCenter
from pageObject.logout import logout
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.mark.all
class Test_query():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))
        print(self.data)

    @pytest.mark.parametrize()
    def test_1(self,login,bdcdyh,res):
        self.driver = login[0]
        dbInfo = login[1]



        # 办件中心
        taskCenter(self.driver).common()
        # 选择流程
        taskCenter(self.driver).queryCenter()
        # 输入查询数据


    def teardown(self):
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        # # 退出系统
        # logout(self.driver).logout()
        # # 退出浏览器
        # self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'test_houseDyFirstRegister'])
