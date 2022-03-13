from Common.ToolsForOpertion import WebTools
from Common.LogFunc import loggerConf
import time

logger = loggerConf().getLogger()

class taskCenter():
    def __init__(self,driver):
        self.driver = driver

    def common(self):
        # 判断办件中心菜单是否出现
        WebTools(self.driver).check_element_is_exists('xpath', "//div[@xid='mainMenu']/div[1]/div[1]")
        WebTools(self.driver).check_element_is_exists('xpath', "//div[contains(text(),'登记簿查询')]")
        # 办件中心
        WebTools(self.driver).mouse_click('xpath', "//div[@xid='mainMenu']/div[1]/div[1]")
        # 判断新建任务菜单是否出现
        WebTools(self.driver).check_element_is_exists('xpath', "//span[@xid='newTask']")
        # 等待办件中心办件数据加载
        time.sleep(4)
        # 新建任务
        WebTools(self.driver).mouse_click('xpath',"//span[contains(text(),'新建任务')]")
        # 判断新建任务菜单页是否出现
        WebTools(self.driver).check_element_is_exists('link_text', "国有建设用地使用权")

    def chooseNode(self,data):
        '''
        流程发起菜单，包括一级菜单、二级菜单、三级菜单
        :param lcInfo (dict)
            :param qllx: 权利类型,
            :param djlx: 登记类型（optional）
            :param ywlxID: 业务类型ID
        :return:
        '''
        qllx = data.get('initdata').get('lcInfo', None).get('qllx',None)
        djlx = data.get('initdata').get('lcInfo', None).get('djlx', None)
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        if qllx and ywlxID:
            if qllx == '国有建设用地使用权':
                if djlx =='首次登记':
                    # 出让用地
                    if ywlxID == 'C49536D5C50F4F609FACAAAE805EC510':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='C49536D5C50F4F609FACAAAE805EC510']/div[1]")
                        time.sleep(2)
                elif djlx == '转移登记':
                    WebTools(self.driver).mouse_click('xpath',"//ul[@xid='subUl0']/li[2]/a")
                    time.sleep(2)
                    # 转移登记
                    if ywlxID == '7F7384BA05614A0B916BCC8E5C667367':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='7F7384BA05614A0B916BCC8E5C667367']/div[1]")
                        time.sleep(2)
                    # 分割合并转移登记
                    elif ywlxID == '754E1541053249F7B4FFD2F6FD283FC8':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='754E1541053249F7B4FFD2F6FD283FC8']/div[1]")
                        time.sleep(2)
                    # 裁定过户
                    elif ywlxID == '1FD9E9848E0A4059B39F22116F21BD74':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='1FD9E9848E0A4059B39F22116F21BD74']/div[1]")
                        time.sleep(2)
                elif djlx == '变更登记':
                    WebTools(self.driver).mouse_click('xpath',"//ul[@xid='subUl0']/li[3]/a")
                    # 名称、地址、用途等变更登记
                    if ywlxID ==167090000067:
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid=167090000067]/div[1]")
                        time.sleep(2)
                    # 分割合并变更
                    elif ywlxID ==167010001542:
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid=167010001542]/div[1]")
                        time.sleep(2)
                elif djlx == '注销登记':
                    WebTools(self.driver).mouse_click('xpath',"//ul[@xid='subUl0']/li[4]/a")
                    # 注销登记（01401）
                    if ywlxID =='2D8FCFBFEAD4437EB83E00CA35488581':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='2D8FCFBFEAD4437EB83E00CA35488581']/div[1]")
                        time.sleep(2)
            elif qllx == '国有建设用地使用权及房屋所有权':
                WebTools(self.driver).mouse_click('link_text',"国有建设用地使用权及房屋所有权")
                if djlx =='首次登记':
                    # 房屋首次登记
                    if ywlxID == 'F711B2126C44409D903254C246FCD569':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='F711B2126C44409D903254C246FCD569']/div[1]")
                        time.sleep(2)
                    # 自建房屋
                    elif ywlxID == 167090000070:
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid=167090000070]/div[1]")
                        time.sleep(2)
                    # 建筑物区分业主共有部分
                    elif ywlxID == '191B4FB37DD148448BC64944C01A78C1':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='191B4FB37DD148448BC64944C01A78C1']/div[1]")
                        time.sleep(2)
                    # 车库（位）及其他附属设施
                    elif ywlxID == 167090000072:
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid=167090000072]/div[1]")
                        time.sleep(2)
                    # 首次登记（批量）
                    elif ywlxID == '91436F614E6F43409B5A8FE2F0290F8F':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='91436F614E6F43409B5A8FE2F0290F8F']/div[1]")
                        time.sleep(2)
                    # 项目内多幢
                    elif ywlxID == '608286609F5C429CB32BA42C56F7C7F7':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='608286609F5C429CB32BA42C56F7C7F7']/div[1]")
                        time.sleep(2)
                    else:
                        logger.error("%s 业务类型ID不存在！" % ywlxID)
                elif djlx == '转移登记':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl1')]/li[2]/a")
                    # 房屋首次转移登记
                    if ywlxID =='807BD8C295404AA19F2275CB830E5F4C':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='807BD8C295404AA19F2275CB830E5F4C']/div[1]")
                        time.sleep(2)
                    # 存量房转移登记
                    elif ywlxID =='7CEA3E6E7C9D4D4194F77C2FB71FA0A4':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='7CEA3E6E7C9D4D4194F77C2FB71FA0A4']/div[1]")
                        time.sleep(2)
                    # 房的批量转移
                    elif ywlxID =='7E9CABA30D4749D499654390D0ED4DDB':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='7E9CABA30D4749D499654390D0ED4DDB']/div[1]")
                        time.sleep(2)
                    # 预告转现
                    elif ywlxID =='08B6FBC363E745C3ABF0DFDD13ECCD0B':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='08B6FBC363E745C3ABF0DFDD13ECCD0B']/div[1]")
                        time.sleep(2)
                    # 裁定过户（房）
                    elif ywlxID =='E53B3B2C4EE0453D9BCAD57B0107F184':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='E53B3B2C4EE0453D9BCAD57B0107F184']/div[1]")
                        time.sleep(2)
                    # 裁定过户批量（房）
                    elif ywlxID =='BF8570D83B5F4B95A0AD22D9603477D2':
                        time.sleep(2)
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='BF8570D83B5F4B95A0AD22D9603477D2']/div[1]")
                        time.sleep(2)
                    # 分户转移
                    elif ywlxID =='CD62B1699DEB4496AF8D5D5590E945AB':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='CD62B1699DEB4496AF8D5D5590E945AB']/div[1]")
                        time.sleep(2)
                elif djlx == '变更登记':
                    pass
                elif djlx == '注销登记':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl1')]/li[4]/a")
                    # 房屋首次转移登记（含商品房、经适房、安置房）
                    if ywlxID =='7C936E3656FA459DA3EE2F767A18C62F':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='7C936E3656FA459DA3EE2F767A18C62F']/div[1]")
                        time.sleep(2)
                else:
                    print("登记类型（%s）不存在！" % self.djlx)
            elif qllx == '抵押权':
                WebTools(self.driver).mouse_click('link_text',"抵押权")
                if djlx =='首次登记':
                    # 土地抵押
                    if ywlxID == 'F49EEFC631414825BD7B93A84F7A355E':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='F49EEFC631414825BD7B93A84F7A355E']/div[1]")
                        time.sleep(2)
                    # 不动产抵押
                    elif ywlxID == '6DD4B4B44C724FCAAEF3A21BD49E1232':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='6DD4B4B44C724FCAAEF3A21BD49E1232']/div[1]")
                        time.sleep(2)
                    # 在建房地产
                    elif ywlxID == '497903B0B8404E60B70C27DB2C7674F7':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='497903B0B8404E60B70C27DB2C7674F7']/div[1]")
                        time.sleep(2)
                    # 批量抵押（房屋）
                    elif ywlxID == '3394FD609E5F4963AC02AAA07619D535':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='3394FD609E5F4963AC02AAA07619D535']/div[1]")
                        time.sleep(2)
                elif djlx == '转移登记':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl2')]/li[2]/a")
                    # 土地抵押转移
                    if ywlxID == '4845AD57E4034D0AAFFA4E3596DAF094':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='4845AD57E4034D0AAFFA4E3596DAF094']/div[1]")
                        time.sleep(2)
                    # 不动产抵押转移
                    elif ywlxID == '9BAE7B1AC9A0444ABA80C18BFA0F6E59':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='9BAE7B1AC9A0444ABA80C18BFA0F6E59']/div[1]")
                        time.sleep(2)
                    # 在建房地产转移
                    elif ywlxID == 'A0A08B5E60DB461992702483F5D49FA0':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='A0A08B5E60DB461992702483F5D49FA0']/div[1]")
                        time.sleep(2)
                    # 预抵押转现
                    elif ywlxID == '7FCA6894051F46CDBC603DE0E430D1EA':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='7FCA6894051F46CDBC603DE0E430D1EA']/div[1]")
                        time.sleep(2)
                elif djlx == '变更登记':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl2')]/li[3]/a")
                    # 批量抵押变更
                    if ywlxID == 'B99F96081EE34064A11CD70B389CA019':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='B99F96081EE34064A11CD70B389CA019']/div[1]")
                        time.sleep(2)
                else:
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl2')]/li[4]/a")
                    # 不动产抵押注销
                    if ywlxID == 'BAA801115B3740868F1C8824102CABC7':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='BAA801115B3740868F1C8824102CABC7']/div[1]")
                        time.sleep(2)
                    # 土地抵押注销
                    elif ywlxID == '68C62564D96242D5BED0619ED51A0CCC':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='68C62564D96242D5BED0619ED51A0CCC']/div[1]")
                        time.sleep(2)
            elif qllx == '查封登记':
                WebTools(self.driver).mouse_click('link_text', "查封登记")
                if djlx == '查封':
                    # 批量查封
                    if ywlxID == '80E93B91E9974F98AAE75C6AD28629B1':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='80E93B91E9974F98AAE75C6AD28629B1']/div[1]")
                        time.sleep(2)
                    # 批量续查封
                    elif ywlxID == '24A5B1DEA6124BCEA1C38626996BFF97':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='24A5B1DEA6124BCEA1C38626996BFF97']/div[1]")
                        time.sleep(2)
                    # 土地小证查封
                    elif ywlxID == '9549D08993DB44138AC1A433A346C3BC':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='9549D08993DB44138AC1A433A346C3BC']/div[1]")
                        time.sleep(2)
                    # 土地小证续查封
                    elif ywlxID == '819B16A603D4467D882268FF9CE83C02':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='819B16A603D4467D882268FF9CE83C02']/div[1]")
                        time.sleep(2)
                elif djlx == '预查封':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl3')]/li[2]/a")
                    # 预查封（房屋）/批量预售合同查封
                    if ywlxID == 'A7325035C9E24F7784B50AC1E965FFD7' or ywlxID == '7C472DAB0C1D46E1B782689C057B552E':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='A7325035C9E24F7784B50AC1E965FFD7']/div[1]")
                        time.sleep(2)
                    # 批量续预查封
                    if ywlxID == '6559D6E5FB7044D3999FBF2EC76A176B':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='6559D6E5FB7044D3999FBF2EC76A176B']/div[1]")
                        time.sleep(2)
                elif djlx == '解封':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl3')]/li[5]/a")
                    # 批量解封(净地和房地)
                    if ywlxID == '4D22B4174EFD42BCA3C01FE58D9F1477':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='4D22B4174EFD42BCA3C01FE58D9F1477']/div[1]")
                        time.sleep(2)
                    # 批量预解封(房屋)
                    elif ywlxID == '86C66F51F4AB420BBA75221E3B0A7C82':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='4D22B4174EFD42BCA3C01FE58D9F1477']/div[1]")
                        time.sleep(2)
                    # 土地小证解封
                    elif ywlxID == '14B63357509C48C794A471AD88C0531E':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='14B63357509C48C794A471AD88C0531E']/div[1]")
                        time.sleep(2)
                    # 在建工程解封
                    elif ywlxID == 'B489BA1B6E48483EBF1375D877DDE4F4':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='B489BA1B6E48483EBF1375D877DDE4F4']/div[1]")
                        time.sleep(2)
                elif djlx == '司法裁定':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl3')]/li[4]/a")
                    # 批量司法裁定（房和地）
                    if ywlxID == '9AB6783AEDAB4D6CBFF8C7F19D411BE7' or ywlxID == 'EF4D6596ED6347DDA33471FCFA7E973A' :
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='9AB6783AEDAB4D6CBFF8C7F19D411BE7']/div[1]")
                        time.sleep(2)
                    # 预告批量司法裁定（房和地）
                    elif ywlxID == 'AEBFF1F998D846CB932F7CC0ECA0ACAF' or ywlxID == 'EB661D9603EF48E895503BDBC82EADAA':
                        WebTools(self.driver).mouse_doubleClick('xpath',"//div[@ywlxid='AEBFF1F998D846CB932F7CC0ECA0ACAF']/div[1]")
                        time.sleep(2)
                elif djlx == '在建工程查封':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl3')]/li[3]/a")
                    pass
            elif qllx == '其他登记':
                WebTools(self.driver).mouse_click('link_text', "其他登记")
                # 冻结登记（房和地）
                if ywlxID == 'ACAF8531B13B43FC8CB4D521E46FCA58' or ywlxID == 'C2A770118E79445EB50E0108E1BCA69D' :
                    WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='ACAF8531B13B43FC8CB4D521E46FCA58']/div[1]")
                    time.sleep(2)
                # 解冻登记（房和地）
                elif ywlxID == '009B74A8CD6C42C18B6F2C0F16FAC912' or ywlxID == 'CA64F346B5F74F51918D47FA64A00373':
                    WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='009B74A8CD6C42C18B6F2C0F16FAC912']/div[1]")
                    time.sleep(2)
            elif qllx == '预告登记':
                WebTools(self.driver).mouse_click('link_text', "预告登记")
                if djlx =='首次登记':
                    # 商品房预告
                    if ywlxID == '1CEDE7DF7E0F481BB5AF3C8700028F1B':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='1CEDE7DF7E0F481BB5AF3C8700028F1B']/div[1]")
                        time.sleep(2)
                    # 商品房预告抵押
                    elif ywlxID == 'F92E0A9F7CC8429C862DE095D6A04AD4':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='F92E0A9F7CC8429C862DE095D6A04AD4']/div[1]")
                        time.sleep(2)
                    # 净地预告
                    if ywlxID == '4AD2511CA0E14212AFD604CE806B1E9A':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='4AD2511CA0E14212AFD604CE806B1E9A']/div[1]")
                        time.sleep(2)
                elif djlx == '转移登记':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl5')]/li[2]/a")
                elif djlx == '变更登记':
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl5')]/li[3]/a")
                else:
                    WebTools(self.driver).mouse_click('xpath', "//ul[contains(@xid,'subUl5')]/li[4]/a")
                    # 房地预告注销
                    if ywlxID == '8546EB5B8816468B898874A37637D08E':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='8546EB5B8816468B898874A37637D08E']/div[1]")
                        time.sleep(2)
                    # 预告抵押注销
                    elif ywlxID == 'C956D29C47DE4699AD31A620F82961EC':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='C956D29C47DE4699AD31A620F82961EC']/div[1]")
                        time.sleep(2)
                    # 净地预告注销
                    elif ywlxID == '48F888726F514BB5B19ED79663D5CCBE':
                        WebTools(self.driver).mouse_doubleClick('xpath', "//div[@ywlxid='48F888726F514BB5B19ED79663D5CCBE']/div[1]")
                        time.sleep(2)
        else:
            logger.error("权利类型和业务类型ID参数必填。")

    def queryCenter(self):
        WebTools(self.driver).mouse_click('xpath',"//div[@title='查询中心']")
        time.sleep(2)
