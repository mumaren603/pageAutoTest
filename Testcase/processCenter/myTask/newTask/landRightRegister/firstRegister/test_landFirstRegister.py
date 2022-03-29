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
from pageObject.submitPage import submitPage
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.szfzPage import szfzPage
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.mark.all
class Test_landFirstRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))

    def test_landFristRegister(self,openProcessCenter):
        '''
        :流程 国有建设用地使用权--首次登记--出让登记
        :return:
        '''
        self.driver = openProcessCenter
        # 获取办件数据
        bdcdyh = dataInit().getLandCqNotRegisterData(self.data)
        logger.debug("<--------国有建设用地使用权--首次登记--出让登记start-------->")
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
        # sflzbPage(self.driver).sflzbHandle(cmdopt)
        # 办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 审核
        submitPage(self.driver).shHandle(bdcdyh)
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh)
        # # 制证
        # szfzPage(self.driver).szHandle(bdcdyh,cmdopt)
        # # 发证
        # szfzPage(self.driver).fzHandle(bdcdyh,cmdopt)
        logger.debug("<--------界面操作end------->")

        try:
            logger.debug("<--------归档数据检查start-------->")
            resDataCheck = dataResCheck().landRegisterDataCheck(bdcdyh,self.data)
            assert resDataCheck
            logger.debug("<--------归档数据检查end-------->")
        except AssertionError:
            raise
        logger.debug("<--------国有建设用地使用权--首次登记--出让登记end-------->")

    # def teardown(self):
    #     logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    #     # 退出系统
    #     logout(self.driver).logout()
    #     # 退出浏览器
    #     self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v','test_landFristRegister'])
