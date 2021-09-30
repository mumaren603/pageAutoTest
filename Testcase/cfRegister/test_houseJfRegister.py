import pytest,os
from init.dataInit import dataInit
from pageObject.taskCenter import taskCenter
from pageObject.queryFunc import queryFunc
from pageObject.sjdPage import sjdPage
from pageObject.sqbPage import sqbPage
from pageObject.blyjPage import blyjPage
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.submitPage import submitPage
from Common.logFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.mark.smoke
@pytest.mark.all
class Test_houseJfRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\', '/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))

    def test_houseJfRegister(self,login,cmdopt):
        '''
        :流程 查封登记--解封登记（房屋）
        :return:
        '''
        logger.debug("<--------查封登记-->解封登记（房屋）-------->")
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit(dbInfo).getHouseXcfRegisterData()

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
        # 办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh, self.data)
        # 登出
        logout(self.driver).logout()

        # 数据库校验
        logger.debug("<--------归档数据检查-------->")
        try:
            resDataCheck = dataResCheck(dbInfo).jfRegisterDataCheck(bdcdyh,self.data)
            assert resDataCheck
        except AssertionError:
            raise

    def teardown(self):
        self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'test_houseJfRegister'])



