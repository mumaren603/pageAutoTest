import time
from Common.ToolsForOpertion import WebTools
from init.userInfoInit import generateAddr,generateCertNum,generateDYQLRName,generateTelnum,generateQLRName

class sqrqkPage():
    def __init__(self,driver):
        self.driver = driver

    def sqrqkHandle(self,data):
        '''
        封装流程受理（申请人情况）
        :param data (dict)
            :param lcInfo (dict)
                :param qllx: 权利类型,
                :param djlx: 登记类型（optional）
                :param ywlxID: 业务类型ID
        :return:
        '''
        qllx = data.get('initdata').get('lcInfo',None).get('qllx',None)
        djlx = data.get('initdata').get('lcInfo', None).get('djlx', None)
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        ygType = data.get('initdata').get('params', None).get('ygType', None)

        WebTools(self.driver).check_element_is_exists('link_text','申请人情况')
        WebTools(self.driver).mouse_click('link_text', '申请人情况')
        # 将页面滚动条拖到顶部
        self.driver.execute_script("document.documentElement.scrollTop=0")
        WebTools(self.driver).check_element_is_exists('xpath',"//th[contains(text(),'是否通知人')]")

        # 动态获取权利人数据
        qlrmc = generateQLRName()
        dyQlrmc = generateDYQLRName()
        qlrzjhm = generateCertNum()
        qlrdhhm = generateTelnum()
        qlrtxdz = generateAddr()

        if qllx =='国有建设用地使用权' or qllx == '国有建设用地使用权及房屋所有权':
            if djlx == '首次登记':
                WebTools(self.driver).mouse_click('xpath', "//div[contains(text(),'申请人信息')]/..//*[contains(text(),'新增')]")
                time.sleep(1)
                # 姓名
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", qlrmc)
                # 是否通知
                WebTools(self.driver).mouse_click('name', 'SFTZR')
                # 证件类型
                WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath', "//select[@name='SQRZJZL']/option[4]")
                # 证件号码
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                # 电话
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                # 通讯地址
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRTXDZ']", qlrtxdz)
                # 共有方式
                WebTools(self.driver).choose_droplist_value('GYFS', 'xpath', "//select[@name='GYFS']/option[2]")
            elif djlx == '转移登记':
                # 预转现，裁定过户（地），裁定过户批量（地），裁定过户（房），裁定过户批量（房 ）
                qlrlist=[
                         '08B6FBC363E745C3ABF0DFDD13ECCD0B',
                         '1FD9E9848E0A4059B39F22116F21BD74',
                         '1652988554BE4119B4B86334F18552AF',
                         'E53B3B2C4EE0453D9BCAD57B0107F184',
                         'BF8570D83B5F4B95A0AD22D9603477D2'
                         ]
                if ywlxID in qlrlist:
                # if ywlxID == '08B6FBC363E745C3ABF0DFDD13ECCD0B' or ywlxID == 'E53B3B2C4EE0453D9BCAD57B0107F184' or ywlxID == 'BF8570D83B5F4B95A0AD22D9603477D2':
                    WebTools(self.driver).check_element_is_exists('xpath', "//table[@xid='underTable']/tbody/tr[1]/td[9]//span[contains(text(),'编辑')]")
                    WebTools(self.driver).mouse_click('xpath', "//table[@xid='underTable']/tbody/tr[1]/td[9]//span[contains(text(),'编辑')]")
                    time.sleep(1)
                    # 是否通知
                    WebTools(self.driver).mouse_click('name', 'SFTZR')
                    # 证件类型
                    WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath',"//select[@name='SQRZJZL']/option[4]")
                    # 证件号码
                    WebTools(self.driver).input_clear('xpath', "//input[@xid='SQRZJH']")
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                    # 电话
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                else:
                    WebTools(self.driver).check_element_is_exists('xpath', "//div[contains(text(),'权利人列表')]/../div[2]/span[3]")
                    time.sleep(2)
                    WebTools(self.driver).mouse_click('xpath', "//div[contains(text(),'权利人列表')]/../div[2]/span[3]")
                    time.sleep(1)
                    # 姓名
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", qlrmc)
                    # 是否通知
                    WebTools(self.driver).mouse_click('name', 'SFTZR')
                    # 证件类型
                    WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath',"//select[@name='SQRZJZL']/option[4]")
                    # 证件号码
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                    # 电话
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                    # 通讯地址
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRTXDZ']", qlrtxdz)
                    # 共有方式
                    WebTools(self.driver).choose_droplist_value('GYFS', 'xpath', "//select[@name='GYFS']/option[2]")
        elif qllx == '抵押权':
            if djlx == '首次登记':
                # 在建工程抵押首次
                if ywlxID == 167090000093:
                    # 打印当前操作界面的句柄
                    current_handle = self.driver.current_window_handle
                    print('current_handle', current_handle)
                    # 获取当前打开页的所有句柄并打印，应该只有一个
                    all_handles = self.driver.window_handles
                    print('all_handles', all_handles)

                    # 新增预告抵押人
                    WebTools(self.driver).mouse_click('xpath', "//div[contains(text(),'预告抵押人列表')]/../div[2]/span[1]")
                    time.sleep(4)  # 强制等待2秒

                    # 获取进入新窗口后所有的句柄，并打印当前所有的句柄，此次应该有两个了
                    all_handles2 = self.driver.window_handles
                    print('all_handles2', all_handles2)
                    self.driver.implicitly_wait(2)

                    # 拿到新窗口句柄
                    newhandle = [handle for handle in all_handles2 if handle not in all_handles]
                    # 打印新窗口
                    print('newhandle', newhandle[0])
                    # 切换到新窗口
                    self.driver.switch_to.window(newhandle[0])
                    time.sleep(2)
                    # 打印新窗口的title
                    print('新窗口的title：', self.driver.title)

                    # WebTools(self.driver).current_handle()
                    # 姓名
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", '绿地中国地产开发有限公司')
                    # 证件类型
                    WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath', "//select[@name='SQRZJZL']/option[8]")
                    # 证件号码
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", '999999999991N')
                    # 保存
                    # # 新增预告抵押权人
                    # WebTools(self.driver).mouse_click('xpath', "//div[contains(text(),'预告抵押权人列表')]/../div[2]/span[2]")
                    # # 姓名
                    # WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", qlrmc)
                    # # 证件类型
                    # WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath', "//select[@name='SQRZJZL']/option[8]")
                    # # 证件号码
                    # WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                else:
                    # 将页面滚动条拖到指定元素（抵押权人列表）
                    WebTools(self.driver).srollBarToElement("//*[contains(text(),'抵押权人列表')]")
                    WebTools(self.driver).check_element_is_exists('xpath', "//div[contains(text(),'抵押权人列表')]/../div[2]/span[3]")
                    WebTools(self.driver).mouse_click('xpath','//table[@xid="underTable"]//span[contains(text(),"新增")]')
                    time.sleep(1)
                    # 姓名
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", dyQlrmc)
                    # 是否通知
                    WebTools(self.driver).mouse_click('name', 'SFTZR')
                    # 证件类型
                    WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath',"//select[@name='SQRZJZL']/option[4]")
                    # 证件号码
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                    # 电话
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                    # 共有方式
                    WebTools(self.driver).choose_droplist_value('GYFS', 'xpath', "//select[@name='GYFS']/option[2]")
                    # 通讯地址
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRTXDZ']", qlrtxdz)
            elif djlx =='转移登记':
                # 预抵押转现
                if ywlxID == '7FCA6894051F46CDBC603DE0E430D1EA':
                    WebTools(self.driver).mouse_click('xpath',"//table[contains(@xid,'underTable')]//span[contains(text(),'编辑')]")
                    # 将页面滚动条拖到指定元素（登记原因）
                    WebTools(self.driver).srollBarToElement("//input[@xid='ZJYXQ']")
                    # 是否通知
                    WebTools(self.driver).mouse_click('name', 'SFTZR')
                    # 电话
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                else:
                    self.driver.execute_script("document.documentElement.scrollTop=250")
                    WebTools(self.driver).check_element_is_exists('xpath',"//div[contains(text(),'抵押权人列表')]/../div[2]/span[3]")
                    WebTools(self.driver).mouse_click('xpath','//table[@xid="underTable"]//span[contains(text(),"新增")]')
                    time.sleep(1)
                    # 姓名
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", dyQlrmc)
                    # 是否通知
                    WebTools(self.driver).mouse_click('name', 'SFTZR')
                    # 证件类型
                    WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath',"//select[@name='SQRZJZL']/option[4]")
                    # 证件号码
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                    # 电话
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                    # 共有方式
                    WebTools(self.driver).choose_droplist_value('GYFS', 'xpath', "//select[@name='GYFS']/option[2]")
                    # 通讯地址
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRTXDZ']", qlrtxdz)
            elif djlx == '变更登记':
                WebTools(self.driver).mouse_click('xpath', "//table[contains(@xid,'underTable')]//tr[1]/td[9]//span[1]")
                self.driver.execute_script("document.documentElement.scrollTop=250")
                time.sleep(1)
                # 是否通知
                WebTools(self.driver).mouse_click('name', 'SFTZR')
                # 电话
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                # 在建房地产
            else:
                pass

        elif qllx == '预告登记':
            if djlx == '首次登记':
                # 预告和预抵义务人操作
                # if ywlxID == 167090000093:
                #     # 打印当前操作界面的句柄
                #     current_handle = self.driver.current_window_handle
                #     print('current_handle', current_handle)
                #     # 获取当前打开页的所有句柄并打印，应该只有一个
                #     all_handles = self.driver.window_handles
                #     print('all_handles', all_handles)
                #
                #     # 新增预告抵押人
                #     WebTools(self.driver).mouse_click('xpath', "//div[contains(text(),'预告抵押人列表')]/../div[2]/span[1]")
                #     time.sleep(4)  # 强制等待2秒
                #
                #     # 获取进入新窗口后所有的句柄，并打印当前所有的句柄，此次应该有两个了
                #     all_handles2 = self.driver.window_handles
                #     print('all_handles2', all_handles2)
                #     self.driver.implicitly_wait(2)
                #
                #     # 拿到新窗口句柄
                #     newhandle = [handle for handle in all_handles2 if handle not in all_handles]
                #     # 打印新窗口
                #     print('newhandle', newhandle[0])
                #     # 切换到新窗口
                #     self.driver.switch_to.window(newhandle[0])
                #     time.sleep(2)
                #     # 打印新窗口的title
                #     print('新窗口的title：', self.driver.title)
                #
                #     # WebTools(self.driver).current_handle()
                #     # 姓名
                #     WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", '绿地中国地产开发有限公司')
                #     # 证件类型
                #     WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath', "//select[@name='SQRZJZL']/option[8]")
                #     # 证件号码
                #     WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", '999999999991N')
                #     # 保存
                #     # # 新增预告抵押权人
                #     # WebTools(self.driver).mouse_click('xpath', "//div[contains(text(),'预告抵押权人列表')]/../div[2]/span[2]")
                #     # # 姓名
                #     # WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", qlrmc)
                #     # # 证件类型
                #     # WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath', "//select[@name='SQRZJZL']/option[8]")
                #     # # 证件号码
                #     # WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                # 预抵押
                if ygType == 1:
                    self.driver.execute_script("document.documentElement.scrollTop=250")
                    WebTools(self.driver).check_element_is_exists('xpath',"//div[contains(text(),'抵押权人列表')]/../div[2]/span[3]")
                    WebTools(self.driver).mouse_click('xpath', '//table[@xid="underTable"]//span[contains(text(),"新增")]')
                    time.sleep(1)
                    # 姓名
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", dyQlrmc)
                # 预告
                else:
                    WebTools(self.driver).check_element_is_exists('xpath',"//div[contains(text(),'预告权利人列表')]/../div[2]/span[3]")
                    WebTools(self.driver).mouse_click('xpath', '//table[@xid="underTable"]//span[contains(text(),"新增")]')
                    time.sleep(1)
                    # 姓名
                    WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", qlrmc)
                # 是否通知
                WebTools(self.driver).mouse_click('name', 'SFTZR')
                # 证件类型
                WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath', "//select[@name='SQRZJZL']/option[4]")
                # 证件号码
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                # 电话
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                # 共有方式
                WebTools(self.driver).choose_droplist_value('GYFS', 'xpath', "//select[@name='GYFS']/option[2]")
                # 通讯地址
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRTXDZ']", qlrtxdz)
            else:
                pass
        elif qllx == '查封登记':
            if djlx == '司法裁定':
                WebTools(self.driver).mouse_click('xpath', "//div[contains(text(),'申请人信息')]/../div[2]/span[3]")
                time.sleep(1)
                # 姓名
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRMC']", qlrmc)
                # 是否通知
                WebTools(self.driver).mouse_click('name', 'SFTZR')
                # 证件类型
                WebTools(self.driver).choose_droplist_value('SQRZJZL', 'xpath', "//select[@name='SQRZJZL']/option[4]")
                # 证件号码
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRZJH']", qlrzjhm)
                # 电话
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRDHHM']", qlrdhhm)
                # 通讯地址
                WebTools(self.driver).input_content('xpath', "//input[@xid='SQRTXDZ']", qlrtxdz)
                # 共有方式
                WebTools(self.driver).choose_droplist_value('GYFS', 'xpath', "//select[@name='GYFS']/option[2]")

        # 公共操作
        if djlx != '注销登记':
            # 将页面滚动条拖到顶部
            self.driver.execute_script("document.documentElement.scrollTop=50")
            time.sleep(1)
            # 保存
            WebTools(self.driver).mouse_click('xpath', "//span[@xid='saveBtn']")
            # 校验保存按钮点击后页面弹出框
            WebTools(self.driver).allow_element_is_exists('class_name', 'BeAlert_box')



