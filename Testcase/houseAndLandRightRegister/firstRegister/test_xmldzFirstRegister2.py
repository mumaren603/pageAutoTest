'''
国有建设用地使用权及房屋所有权 -- 首次登记 -- 建筑物区分业主共有部分（02103）
'''
import pytest,os
from init.dataInit import dataInit
from pageObject.taskCenter import taskCenter
from pageObject.queryFunc import queryFunc
from pageObject.sjdPage import sjdPage
from pageObject.sqrqkPage import sqrqkPage
from init.userInfoInit import generateAddr,generateCertNum,generateQLRName,generateTelnum
from pageObject.sqbPage import sqbPage
from pageObject.bdcjbxxPage import bdcjbxxPage
from pageObject.blyjPage import blyjPage
from pageObject.submitPage import submitPage
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck
from utils.getTestdata import getTestcaseData,getTestdataPath
from Common.logFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.mark.test
@pytest.mark.all
class Test_xmldzFirstRegister2():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))

    def test_xmldzFristRegister2(self,login,cmdopt):
        '''
        :流程 国有建设用地使用权及房屋所有权--首次登记--建筑物区分业主共有部分
        :发起流程bdcdyh作为主产权数据，通过getXmldzFirstRegisterData()获取，不动产基本信息页面添加产权通过getXmldzFirstRegisterData2()获取
        :return:
        '''
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit(dbInfo).getXmldzFirstRegisterData()
        bdcdyh2 = dataInit(dbInfo).getXmldzFirstRegisterData2(bdcdyh)

        logger.debug("<--------国有建设用地使用权及房屋所有权--首次登记--项目类多幢（按幢发证）start-------->")
        logger.debug("<--------界面操作start-------->")

        #办件中心
        taskCenter(self.driver).common()
        #选择流程
        taskCenter(self.driver).chooseNode(self.data)
        #发起查询
        queryFunc(self.driver).query(bdcdyh, self.data)
        #收件单
        sjdPage(self.driver).sjdHandle(self.data)
        #申请人情况
        sqrqkPage(self.driver).sqrqkHandle(self.data)
        #申请表
        sqbPage(self.driver).sqbHandle(self.data)
        #不动产基本信息
        bdcjbxxPage(self.driver).bdcjbxxHandle(self.data,bdcdyh2)
        # #收费领证表
        # sflzbPage(self.driver).sflzbHandle(self.sfTemplate)
        #办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 审核
        submitPage(self.driver).shHandle(bdcdyh)
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh,self.data)
        logger.debug("<--------界面操作end------->")

        # 数据库验证
        try:
            logger.debug("<--------归档数据检查start-------->")
            resDataCheck = dataResCheck(dbInfo).xmldzRegisterDataCheck2(bdcdyh,self.data)
            assert resDataCheck
            logger.debug("<--------归档数据检查end-------->")
        except AssertionError:
            raise
        logger.debug("<--------国有建设用地使用权及房屋所有权--首次登记--项目类多幢（按幢发证）end-------->")

    def teardown(self):
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        # 退出系统
        logout(self.driver).logout()
        # 退出浏览器
        self.driver.quit()


if __name__ == '__main__':
    pytest.main(['-v', 'test_xmldzFristRegister2'])
