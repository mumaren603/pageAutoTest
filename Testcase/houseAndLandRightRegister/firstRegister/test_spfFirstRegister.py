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
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.submitPage import submitPage
from Common.logFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.mark.test
@pytest.mark.all
class Test_spfFirstRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        self.data = getTestcaseData(getTestdataPath(current_file_path))

    def test_spfFristRegister(self,login,cmdopt):
        '''
        :流程 国有建设用地使用权及房屋所有权--首次登记--房屋首次登记
        :param login: 装饰器，登录操作封装，返回信息：(1) webdriver对象（2）数据库配置信息 例如：(<selenium.webdriver.chrome.webdriver.WebDriver (session="f8c32afd6fd5c944984d9aeaadfa9341")>,
         {'dj': '172.16.17.247:1521/tzdj', 'qj': '172.16.17.247:1521/tzkjk'})
        :return:
        '''
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit(dbInfo).getSpfFirstRegisterData()
        logger.debug("#####国有建设用地使用权及房屋所有权--首次登记--房屋首次登记")
        logger.debug(">>>>>界面操作start<<<<<")

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
        # 不动产基本信息
        bdcjbxxPage(self.driver).bdcjbxxHandle(self.data)
        # 收费领证表
        # sflzbPage(self.driver).sflzbHandle()
        # 办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 复审
        submitPage(self.driver).shHandle(bdcdyh)
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh, self.data)
        logger.debug(">>>>>界面操作end<<<<<")

        # 数据库验证
        try:
            logger.debug("<--------归档数据检查start-------->")
            resDataCheck = dataResCheck(dbInfo).houseRegisterDataCheck(bdcdyh,self.data)
            assert resDataCheck
            logger.debug("<--------归档数据检查end-------->")
        except AssertionError:
            raise

    def teardown(self):
        logger.debug(">>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<")
        # 退出系统
        logout(self.driver).logout()
        # 退出浏览器
        self.driver.quit()


if __name__ == '__main__':
    pytest.main(['-v', 'test_spfFristRegister'])
