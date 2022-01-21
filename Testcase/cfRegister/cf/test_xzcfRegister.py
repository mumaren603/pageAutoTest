import pytest,os
from init.dataInit import dataInit
from pageObject.bdcjbxxPage import bdcjbxxPage
from pageObject.taskCenter import taskCenter
from pageObject.queryFunc import queryFunc
from pageObject.sjdPage import sjdPage
from pageObject.sqbPage import sqbPage
from pageObject.blyjPage import blyjPage
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.submitPage import submitPage
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.mark.test
class Test_xzcfRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\', '/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))

    def test_xzcfRegister(self,login,cmdopt):
        '''
        :流程 查封登记--查封--土地小证查封
        :return:
        '''
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit().getXzcfRegisterData()
        logger.debug("<--------查封登记--查封--土地小证查封start-------->")
        logger.debug("<--------界面操作start-------->")

        # 办件中心
        taskCenter(self.driver).common()
        # 选择流程
        taskCenter(self.driver).chooseNode(self.data)
        # 发起查询
        queryFunc(self.driver).query(bdcdyh, self.data)
        # 收件单
        sjdPage(self.driver).sjdHandle(self.data)
        # 申请表
        sqbPage(self.driver).sqbHandle(self.data)
        # 不动产基本信息
        bdcjbxxPage(self.driver).bdcjbxxHandle(self.data)
        # 办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh, self.data)
        logger.debug("<--------界面操作end-------->")

        # 数据库校验
        try:
            logger.debug("<--------归档数据检查start-------->")
            resDataCheck = dataResCheck().xzcfRegisterDataCheck(bdcdyh,self.data)
            assert resDataCheck
            logger.debug("<--------归档数据检查end-------->")
        except AssertionError:
            raise
        logger.debug("<--------查封登记--查封--土地小证查封end-------->")

    def teardown(self):
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        # 退出系统
        logout(self.driver).logout()
        # 退出浏览器
        self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'test_xzcfRegister'])


