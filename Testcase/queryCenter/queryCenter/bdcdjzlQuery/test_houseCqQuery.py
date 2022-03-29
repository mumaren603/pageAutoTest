import pytest,os
from utils.getTestdataForJson import getTestcaseData,getTestdataPath
from Common.ToolsForOpertion import WebTools
from init.dataInit import dataInit
from Common.LogFunc import loggerConf
logger = loggerConf().getLogger()

data = getTestcaseData(getTestdataPath(os.path.abspath(__file__).replace('\\', '/')))

@pytest.mark.all
class Test_houseCqQuery():
    # 输入正确查询条件，查询结果正确，正常出产调证明
    def test_houseCqQuery_1(self,openQueryCenter):
        # global driver
        # driver = openQueryCenter[0]
        driver = openQueryCenter
        bdcdyh = dataInit().getHouseCqRegisterData()
        WebTools(driver).mouse_click('xpath',"//th[contains(text(),'查询条件')]/..//label[2]/span[1]")
        WebTools(driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",bdcdyh)
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'"+ bdcdyh +"')]/../../../td[1]//input[@type='checkbox']")
        WebTools(driver).mouse_click('xpath',"//span[(text()='现势信息')]/..//span[contains(text(),'登记证明')]")
        import time
        time.sleep(2)

        val= WebTools(driver).is_element_exist("//*[@id='viewer']")
        assert val

    # 产权有抵押，查询正确
    def test_houseCqQuery_2(self,openQueryCenter):
        driver = openQueryCenter
        sql = data.get('test_houseCqQuery_1').get('params').get('sql')
        bdcdyh = dataInit().getHouseDyRegisterData()
        WebTools(driver).mouse_click('xpath',"//th[contains(text(),'查询条件')]/..//label[2]/span[1]")
        WebTools(driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",bdcdyh)
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")
        res = WebTools(driver).is_element_exist("//span[text()='"+ bdcdyh +"'] /../../../td[7]//span[text()='有']")
        assert res

    # 产权有查封，查询正确
    def test_houseCqQuery_3(self,openQueryCenter):
        driver = openQueryCenter
        sql = data.get('test_houseCqQuery_1').get('params').get('sql')
        bdcdyh = dataInit().getHouseCfRegisterData()
        WebTools(driver).mouse_click('xpath',"//th[contains(text(),'查询条件')]/..//label[2]/span[1]")
        WebTools(driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",bdcdyh)
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")
        res = WebTools(driver).is_element_exist("//span[text()='"+ bdcdyh +"'] /../../../td[8]//span[text()='有']")
        assert res

    # 输入错误人名，正确身份证号码，查询房屋为空，出具无房证明
    @pytest.mark.parametrize('qlrmc,qlrzjhm',[(data.get('test_houseCqQuery_3').get('params').get('qlrmc'),
                                               data.get('test_houseCqQuery_3').get('params').get('qlrzjhm'))
                                              ])
    def test_houseCqQuery_4(self,qlrmc,qlrzjhm,openQueryCenter):
        driver = openQueryCenter
        print(qlrmc,qlrzjhm)
        WebTools(driver).input_content('xpath',"//th[text()='权利人姓名']/../td[1]//input",qlrmc)
        WebTools(driver).input_content('xpath', "//th[text()='权利人证件号码']/../td[1]//input",qlrzjhm)
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")
        val= WebTools(driver).is_element_exist("//div[@class='ivu-table-body ivu-table-overflowX']")
        assert val == False

    def test_houseCqQuery_5(self,openQueryCenter):
        driver = openQueryCenter
        WebTools(driver).mouse_click('xpath',"//th[contains(text(),'查询条件')]/..//label[2]/span[1]")
        WebTools(driver).input_clear('xpath',"//label[contains(text(),'不动产单元号')]/..//input")
        WebTools(driver).input_content('xpath',"//label[contains(text(),'不动产单元号')]/..//input",'12312312312')
        WebTools(driver).mouse_click('xpath',"//span[contains(text(),'点击生成受理编号')]")
        WebTools(driver).mouse_click('xpath', "//span[contains(text(),'下一步')]")

    # def teardown_class(self):
    #     logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行end<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    #     # 退出系统
    #     logout(driver).logout()
    #     # 退出浏览器
    #     driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', 'Test_houseCqQuery'])
