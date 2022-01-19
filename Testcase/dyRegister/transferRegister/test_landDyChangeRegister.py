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
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.submitPage import submitPage
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck

@pytest.mark.all
class Test_landDyChangeRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        print("当前测试用例路径是:%s" % current_file_path)
        data = getTestcaseData(getTestdataPath(current_file_path))
        self.lcInfo = data.get('initdata').get('lcInfo')
        self.params = data.get('initdata').get('params')

    def test_landDyChangeRegister(self,login,cmdopt):
        '''
        :流程 抵押权--转移登记--土地抵押转移（03201）
        '''
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit().getLandDyChangeRegisterData()
        print("办件受理数据为：%s" % bdcdyh)

        # 办件中心
        taskCenter(self.driver).common()
        # 选择流程
        taskCenter(self.driver).chooseNode(self.lcInfo)
        # 发起查询
        queryFunc(self.driver).query(bdcdyh,self.lcInfo, self.params)
        # 收件单
        sjdPage(self.driver).sjdHandle(cmdopt, self.lcInfo, self.params)
        # 申请人情况
        sqrqkPage(self.driver).sqrqkHandle(self.lcInfo)
        # 申请表
        sqbPage(self.driver).sqbHandle(self.lcInfo, self.params)
        # 不动产基本信息
        bdcjbxxPage(self.driver).bdcjbxxHandle()
        # 收费领证表
        sflzbPage(self.driver).sflzbHandle(cmdopt)
        # 办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 审核
        submitPage(self.driver).shHandle(bdcdyh)
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh)

        # 数据库验证
        try:
            resDataCheck = dataResCheck().dyRegisterDataCheck(bdcdyh, self.lcInfo)
            print("数据库检查结果是：", resDataCheck)
            assert resDataCheck
        except AssertionError:
            raise

    def teardown(self):
        # 退出系统
        logout(self.driver).logout()
        # 退出浏览器
        self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'test_landDyChangeRegister'])