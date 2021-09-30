import pytest,os
from init.dataInit import dataInit
from pageObject.taskCenter import taskCenter
from pageObject.queryFunc import queryFunc
from pageObject.sqrqkPage import sqrqkPage
from init.userInfoInit import generateAddr,generateCertNum,generateDYQLRName,generateTelnum
from pageObject.sqbPage import sqbPage
from pageObject.bdcjbxxPage import bdcjbxxPage
from pageObject.sflzbPage import sflzbPage
from pageObject.blyjPage import blyjPage
from utils.getTestdata import getTestcaseData,getTestdataPath
from pageObject.submitPage import submitPage
from pageObject.logout import logout


# 预告抵押人未处理
@pytest.mark.skip()
class Test_zjfdcDyFirstRegister():
    def setup(self):
        '''初始化用户数据获取'''
        current_file_path = os.path.abspath(__file__).replace('\\','/')
        print("当前测试用例路径是:%s" % current_file_path)
        data = getTestcaseData(getTestdataPath(current_file_path))
        self.lcInfo = data.get('initdata').get('lcInfo')
        self.params = data.get('initdata').get('params')
        self.qlrParams = {
            "ywlxNode": "dyRegister",
            "qlrmc": generateDYQLRName(),
            "qlrzjhm": generateCertNum(),
            "qlrdhhm": generateTelnum(),
            "qlrtxdz": generateAddr()
        }

    def test_zjfdcDyFirstRegister(self,login,cmdopt):
        '''
        :流程 抵押权--首次登记--在建房地产（03103）
        '''
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit(dbInfo).getZjfdcFirstDyRegisterData()
        print("办件受理数据为：%s" % bdcdyh)

        # 办件中心
        taskCenter(self.driver).common()
        # 选择流程
        taskCenter(self.driver).chooseNode(self.lcInfo)
        # 发起查询
        queryFunc(self.driver).query(bdcdyh, self.lcInfo, self.params)
        # 申请人情况
        sqrqkPage(self.driver).sqrqkHandle(self.lcInfo, self.qlrParams)
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
        submitPage(self.driver).shHandle(bdcdyh, cmdopt, self.splc)
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh)
        # 登出
        logout(self.driver).logout()

        # # 数据库验证
        # qlrmc = self.qlrParams.get("qlrmc")
        # if qlrmc:
        #     try:
        #         resDataCheck = dataResCheck(dbInfo).dyRegisterDataCheck(bdcdyh, qlrmc)
        #         print("数据库检查结果是：", resDataCheck)
        #         assert resDataCheck
        #     except AssertionError:
        #         raise

    def teardown(self):
        self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'test_zjfdcDyFirstRegister'])
