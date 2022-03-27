import pytest,os
from init.dataInit import dataInit
from pageObject.taskCenter import taskCenter
from pageObject.queryFunc import queryFunc
from pageObject.sjdPage import sjdPage
from pageObject.sqrqkPage import sqrqkPage
from pageObject.sqbPage import sqbPage
from pageObject.bdcjbxxPage import bdcjbxxPage
from pageObject.sflzbPage import sflzbPage
from pageObject.blyjPage import blyjPage
from pageObject.htxxPage import htxxPage
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.submitPage import submitPage
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.mark.all
class Test_landCancelRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))

    def test_landCancelRegister(self,openProcessCenter):
        '''
        :流程 国有建设用地使用权--注销登记--注销登记
        '''
        self.driver = openProcessCenter[0]
        # 获取办件数据
        bdcdyh = dataInit().getLandCqRegisterData(self.data)
        logger.debug("<--------国有建设用地使用权--注销登记--注销登记start-------->")
        logger.debug("<--------界面操作start-------->")

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
        # 不动产基本信息
        bdcjbxxPage(self.driver).bdcjbxxHandle(self.data)
        # 收费领证表
        # sflzbPage(self.driver).sflzbHandle()
        # 询问笔录
        # htxxPage(self.driver).xwjlHandle()
        # 办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh)
        logger.debug("<--------界面操作end------->")

        # 数据库校验
        try:
            logger.debug("<--------归档数据检查start-------->")
            resDataCheck = dataResCheck().landCancelRegisterDataCheck(bdcdyh, self.data)
            assert resDataCheck
            logger.debug("<--------归档数据检查end-------->")
        except AssertionError:
            raise
        logger.debug("<--------国有建设用地使用权--注销登记--注销登记end-------->")
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    # def teardown(self):
    #     logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    #     # 退出系统
    #     logout(self.driver).logout()
    #     # 退出浏览器
    #     self.driver.quit()


if __name__ == '__main__':
    pytest.main(['-v', 'test_landCancelRegister'])
