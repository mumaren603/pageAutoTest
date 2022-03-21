import pytest,os
from init.dataInit import dataInit
from pageObject.taskCenter import taskCenter
from pageObject.queryFunc import queryFunc
from pageObject.sjdPage import sjdPage
from pageObject.sqrqkPage import sqrqkPage
from pageObject.sqbPage import sqbPage
from pageObject.blyjPage import blyjPage
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.submitPage import submitPage
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.mark.test
@pytest.mark.all
class Test_landPlsfcdRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\', '/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))

    def test_landPlsfcdRegister(self,login,cmdopt):
        '''
        :流程 查封登记--司法裁定批量（净地））-- 不注销抵押
        :return:
        '''
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit().getSfcdRegisterData(self.data)
        logger.debug("<--------查封登记-->司法裁定批量（净地）start-------->")
        logger.debug("<--------界面操作start-------->")

        # 办件中心
        taskCenter(self.driver).common()
        # 选择流程
        taskCenter(self.driver).chooseNode(self.data)
        # 发起查询
        queryFunc(self.driver).query(bdcdyh, self.data)
        # 收件单
        sjdPage(self.driver).sjdHandle(self.data)
        # 申请人情况
        sqrqkPage(self.driver).sqrqkHandle(self.data)
        # 申请表
        sqbPage(self.driver).sqbHandle(self.data)
        # 办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 初审
        submitPage(self.driver).shHandle(bdcdyh)
        # 复审
        submitPage(self.driver).shHandle(bdcdyh)
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh, self.data)
        logger.debug("<--------界面操作end-------->")

        # 数据库校验
        try:
            logger.debug("<--------归档数据检查start-------->")
            resDataCheck = dataResCheck().sfcdRegisterDataCheck(bdcdyh,self.data)
            assert resDataCheck
            logger.debug("<--------归档数据检查end-------->")
        except AssertionError:
            raise
        logger.debug("<--------查封登记-->司法裁定批量（净地）end-------->")

    def teardown(self):
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        # 退出系统
        logout(self.driver).logout()
        # 退出浏览器
        self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'test_landPlsfcdRegister'])



