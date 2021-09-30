import pytest,os
from init.dataInit import dataInit
from pageObject.taskCenter import taskCenter
from pageObject.queryFunc import queryFunc
from pageObject.cancleRegisterCommonPage import cancleRegisterCommonPage
from pageObject.submitPage import submitPage
from dataCheck.dataResCheck import dataResCheck
from utils.getTestdata import getTestcaseData,getTestdataPath


class Test_LandCancelRegister():
    def setup(self):
        current_file_path = os.path.abspath(__file__).replace('\\', '/')
        data = getTestcaseData(getTestdataPath(current_file_path))
        self.qllx = data.get('initdata').get('qllx', None)
        self.djlx = data.get('initdata').get('djlx', None)
        self.ywlx = data.get('initdata').get('ywlx', None)
        self.sfTemplate = data.get('initdata').get('sfTemplate')
        self.splc = data.get('initdata').get('splc')

    def test_landCancelRegister(self,login,cmdopt):
        self.driver = login[0]
        dbInfo = login[1]
        # 获取办件数据
        bdcdyh = dataInit(dbInfo).getLandCancleRegisterData()
        print("办件受理数据为：%s" % bdcdyh)

        # 办件中心
        taskCenter(self.driver).common()
        # 选择流程
        taskCenter(self.driver).chooseNode(self.qllx, self.djlx, self.ywlx)
        # 发起查询
        queryFunc(self.driver).query(bdcdyh, self.qllx, self.djlx)
        # 收件单
        cancleRegisterCommonPage(self.driver).sjdHandle()
        # 申请人情况
        cancleRegisterCommonPage(self.driver).sqrqkHandle()
        # 申请表
        cancleRegisterCommonPage(self.driver).sqbHandle()
        # 不动产基本信息
        cancleRegisterCommonPage(self.driver).bdcjbxxHandle()
        # 受理意见表
        cancleRegisterCommonPage(self.driver).blyjHandle()
        # 受理
        submitPage(self.driver).slHandle()
        # 审核
        submitPage(self.driver).shHandle(bdcdyh,cmdopt,self.splc)
        # 登簿
        submitPage(self.driver).dbHandle(bdcdyh)

        #校验数据库(后期可以把数据库连接串配置化，这样可以针对不同环境校验)
        try:
            resDataCheck = dataResCheck(dbInfo).landCancleRegisterDataCheck(bdcdyh)
            print("数据库检查结果是：",resDataCheck)
            assert resDataCheck
        except AssertionError:
            raise

    def teardown(self):
        self.driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'test_landCancelRegister'])
