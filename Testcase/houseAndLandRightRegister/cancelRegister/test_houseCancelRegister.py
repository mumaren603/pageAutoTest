import pytest,os
from init.dataInit import dataInit
from pageObject.taskCenter import taskCenter
from pageObject.queryFunc import queryFunc
from pageObject.cancleRegisterCommonPage import cancleRegisterCommonPage
from pageObject.blyjPage import blyjPage
from pageObject.htxxPage import htxxPage
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.submitPage import submitPage
from pageObject.logout import logout
from dataCheck.dataResCheck import dataResCheck

@pytest.mark.test
@pytest.mark.all
class Test_houseCancelRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        data = getTestcaseData(getTestdataPath(current_file_path))
        self.lcInfo = data.get('initdata').get('lcInfo')
        self.params = data.get('initdata').get('params')

    def test_houseCancelRegister(self,login,cmdopt):
        '''
        :流程 国有建设用地使用权及房屋所有权--注销登记--注销登记
        '''
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit(dbInfo).getSpfOrClfChangeRegisterData()
        print("办件受理数据为：%s" % bdcdyh)

        # 办件中心
        taskCenter(self.driver).common()
        # 选择流程
        taskCenter(self.driver).chooseNode(self.lcInfo)
        # 发起查询
        queryFunc(self.driver).query(bdcdyh, self.lcInfo, self.params)
        # 收件单
        cancleRegisterCommonPage(self.driver).sjdHandle()
        # 申请人情况
        cancleRegisterCommonPage(self.driver).sqrqkHandle(self.lcInfo)
        # 申请表
        cancleRegisterCommonPage(self.driver).sqbHandle()
        # 不动产基本信息
        cancleRegisterCommonPage(self.driver).bdcjbxxHandle()
        # 询问笔录
        htxxPage(self.driver).xwjlHandle()
        # 办理意见表
        blyjPage(self.driver).blyjHandle()
        # 受理 审核
        submitPage(self.driver).slHandle()
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh, self.params)
        # 登出
        logout(self.driver).logout()

        # 数据库验证
        # try:
        #     resDataCheck = dataResCheck(dbInfo).dyCancelDataCheck(bdcdyh, self.lcInfo)
        #     print("数据库检查结果是：", resDataCheck)
        #     assert resDataCheck
        # except AssertionError:
        #     raise

    # def teardown(self):
    #     self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'test_houseCancelRegister'])
