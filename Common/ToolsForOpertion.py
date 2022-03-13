'''
模拟鼠标单击、双击、键盘输入等操作
'''

import os
import time,datetime
# import allure

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException,TimeoutException,ElementNotVisibleException
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# sys.path.append(ROOT_DIR)

class WebTools(object):
    '''
    封装页面基本操作，如鼠标点击，输入框填写值，校验元素是否存在等
    '''
    def __init__(self,driver):
        self.driver = driver
        self.browser_type = None

    # 截屏
    def save_screenshot(self,img_doc):
        '''
        :param img_doc: 截图说明
        :return:
        '''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\','/')
        errFilename=base_dir+'/errorInfo/error_'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.png'
        self.driver.save_screenshot(errFilename)
        with open(errFilename,mode='rb')as f:
            data = f.read()
        allure.attach(data,img_doc,allure.attachment_type.PNG)

    # 浏览器的设置
    def set_browser(self,testUrl):
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(testUrl)  # 打开被测系统URL
        time.sleep(5)

    # 打开浏览器的方法
    # :param driver_path Driver物理路径
    def open_browser(self,driver_path):
        if self.browser_type == 'Firefox':
            self.driver = webdriver.Firefox(executable_path=driver_path)
        elif self.browser_type == 'Chrome':
            self.driver = webdriver.Chrome(executable_path=driver_path)
        elif self.browser_type == 'IE':
            self.driver = webdriver.Ie(executable_path=driver_path)
        elif self.browser_type == '' or self.browser_type == None:
            logger.error("未指定浏览器类型！")
        self.driver.maximize_window()

    # 跳转页面
    def jump_web_page(self, page, time_wait=3):
        self.driver.get(self.get_web_page(page))
        self.driver.maximize_window()

        if isinstance(time_wait, int):
            time.sleep(time_wait)

    # 滚动条
    # def drag_scrollBar(self,value):
    #     ActionChains(self.driver).move_to_element(value).perform()

    # 浏览器前进操作
    def go_forward(self):
        self.driver.forward()

    # 浏览器后退操作
    def go_back(self):
        self.driver.back()

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    # 保存图片
    def get_windows_img(self,value):
        '''
        在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
        '''
        file_path = os.path.dirname(os.path.abspath('.')) + '/screenshots/'
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
        except NameError as e:
            self.get_windows_img()

    def current_handle(self):
        # 这时切换到新窗口
        all_handles = self.driver.window_handles
        for handle in all_handles:
            self.driver.switch_to.window(handle)

    # 输入内容方法
    def input_content(self, type, value, inputvalue):
        try:
            if type == "xpath":
                self.driver.find_element_by_xpath(value).send_keys(inputvalue)
            elif type == "class_name":
                self.driver.find_element_by_class_name(value).send_keys(inputvalue)
            elif type == "id":
                self.driver.find_element_by_id(value).send_keys(inputvalue)
            elif type == "name":
                self.driver.find_element_by_name(value).send_keys(inputvalue)
            elif type == "link_text":
                self.driver.find_element_by_link_text(value).send_keys(inputvalue)
        except NoSuchElementException as e1:
            logger.error("%s:%s元素未找到" % (type, value))
            self.save_screenshot('查找元素不存在')
            raise e1
        except TimeoutException as e2:
            logger.error("%s:%s元素查找超时" % (type, value))
            self.save_screenshot('查找元素超时')
            raise e2
        except Exception as e:
            logger.error("%s:%s元素查找错误,错误信息：%s" % (type, value, e))
            self.save_screenshot('查找元素错误')
            raise e

    # 下拉框选值
    #:param droplistName 下拉框name名字
    #:param type  下拉框值通过哪种方式选取
    #:param value 下拉框选取具体传值
    def choose_droplist_value(self,droplistName,type,value):
        try:
            if type == "xpath":
                self.driver.find_element_by_name(droplistName).find_element_by_xpath(value).click()
            elif type == "class_name":
                self.driver.find_element_by_name(droplistName).find_element_by_class_name(value).click()
            elif type == "id":
                self.driver.find_element_by_name(droplistName).find_element_by_id(value).click()
            elif type == "name":
                self.driver.find_element_by_name(droplistName).find_element_by_name(value).click()
        except NoSuchElementException as e1:
            logger.error("%s:%s下拉框元素未找到;%s下拉框值选择失败" % (type,droplistName,value))
            self.save_screenshot('下拉框元素未找到。')
            raise e1
        except TimeoutException as e2:
            logger.error("%s:%s元素查找超时" % (type, droplistName))
            self.save_screenshot('查找元素超时')
            raise e2
        except Exception as e:
            logger.error("%s:%s元素查找错误,错误信息：%s" % (type, value,e))
            self.save_screenshot('查找元素错误')
            raise e

    # 鼠标事件(单击)
    def mouse_click(self, type, value):
        try:
            if type == "xpath":
                self.driver.find_element_by_xpath(value).click()
            elif type == "class_name":
                self.driver.find_element_by_class_name(value).click()
            elif type == "id":
                self.driver.find_element_by_id(value).click()
            elif type == "xid":
                self.driver.find_element_by_xid(value).click()
            elif type == "name":
                self.driver.find_element_by_name(value).click()
            elif type == "link_text":
                self.driver.find_element_by_link_text(value).click()
        except NoSuchElementException as e1:
            logger.error("%s:%s元素未找到" % (type, value))
            self.save_screenshot('单击元素未找到')
            raise e1
        except TimeoutException as e2:
            logger.error("%s:%s元素查找超时" % (type, value))
            self.save_screenshot('查找元素超时')
            raise e2
        except Exception as e:
            logger.error("%s:%s元素查找错误,错误信息：%s" % (type, value, e))
            self.save_screenshot('查找元素错误')
            raise e

    # 鼠标事件(双击)
    def mouse_doubleClick(self,type,value):
        try:
            if type == "xpath":
                elm = self.driver.find_element_by_xpath(value)
                ActionChains(self.driver).double_click(elm).perform()
            elif type == "class_name":
                elm = self.driver.find_element_by_class_name(value)
                ActionChains(self.driver).double_click(elm).perform()
            elif type == "id":
                elm = self.driver.find_element_by_id(value)
                ActionChains(self.driver).double_click(elm).perform()
            elif type == "name":
                elm = self.driver.find_element_by_name(value)
                ActionChains(self.driver).double_click(elm).perform()
            elif type == "link_text":
                elm = self.driver.find_element_by_link_text(value)
                ActionChains(self.driver).double_click(elm).perform()
        except NoSuchElementException as e1:
            logger.error("%s:%s元素未找到" % (type, value))
            self.save_screenshot('双击元素未找到。')
            raise e1
        except TimeoutException as e2:
            print("%s:%s元素查找超时" % (type, value))
            logger.error("%s:%s元素查找超时" % (type, value))
            raise e2
        except Exception as e:
            logger.error("%s:%s元素查找错误,错误信息：%s" % (type, value,e))
            self.save_screenshot('查找元素错误')
            raise e

    # 文本框清空
    def input_clear(self, type, value):
        try:
            if type == "xpath":
                self.driver.find_element_by_xpath(value).clear()
            elif type == "id":
                self.driver.find_element_by_id(value).clear()
            elif type == "name":
                self.driver.find_element_by_name(value).clear()
            elif type == "link_text":
                self.driver.find_element_by_link_text(value).clear()
        except NoSuchElementException as e1:
            logger.error("%s:%s元素未找到" % (type, value))
            self.save_screenshot('双击元素未找到。')
            raise e1
        except TimeoutException as e2:
            logger.error("%s:%s元素查找超时" % (type, value))
            raise e2
        except Exception as e:
            logger.error("%s:%s元素查找错误,错误信息：%s" % (type, value, e))
            self.save_screenshot('查找元素错误')
            raise e

    # 允许元素存在（部分数据在某个事件后可能会出现弹出提示，需要点击提示中的确定才可进行以下一步骤操作）
    def allow_element_is_exists(self,type,value):
        try:
            if type == "xpath":
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, value)))
                time.sleep(1)
            elif type == "id":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.ID, value)))
            elif type == "class_name":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, value)))
            elif type == "name":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, value)))
            elif type == "link_text":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.LINK_TEXT, value)))
            WebTools(self.driver).mouse_click('xpath', '//button[@class="BeAlert_confirm"]')
        except:
            pass

    # 验证元素是否存在
    def check_element_is_exists(self, type, value):
        try:
            if type == "xpath":
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH,value)))
                time.sleep(1)
            elif type == "id":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.ID,value)))
            elif type == "class_name":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME,value)))
            elif type == "name":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME,value)))
            elif type == "link_text":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.LINK_TEXT,value)))
        except NoSuchElementException as e1:
            logger.error("%s:%s查找页面元素不存在" %(type,value))
            self.save_screenshot('查找页面元素不存在')
            raise e1
        except TimeoutException as e2:
            logger.error("%s:%s查找页面元素超时" % (type, value))
            self.save_screenshot('查找页面元素超时')
            raise e2
        except ElementNotVisibleException as e3:
            logger.error("%s:%s查找页面元素不可见" % (type, value))
            self.save_screenshot('查找页面元素不可见')
            raise e3
        except Exception as e:
            logger.error("%s:%s元素查找错误,错误信息：%s" % (type, value, e))
            self.save_screenshot('查找页面元素错误')
            raise e

#有问题
    def isElementExist(self,type,value):
        if type == "xpath":
            print(value)
            if len(value) != 0:
                for i in value:
                    print('i:',i)
                    # 元素1  没找到 len=0
                    s = self.driver.find_element_by_xpath(i)
                    if len(s) != 0:
                        return True
                return False
            else:
                print("输入校验ywh的xpath未传递")
        else:
            print("其他校验暂不支持。")

    # 获取子元素
    def select_child_elements(self, type, value1, value2):
        if type == "xpath":
            Select(self.driver.find_element_by_xpath(value1)).select_by_visible_text(value2)
        elif type == "id":
            Select(self.driver.find_element_by_id(value1)).select_by_visible_text(value2)
        elif type == "name":
            Select(self.driver.find_element_by_name(value1)).select_by_visible_text(value2)
        elif type == "link_text":
            Select(self.driver.find_element_by_link_text(value1)).select_by_visible_text(value2)
        elif type == "css_selector":
            Select(self.driver.find_element_by_css_selector(value1)).select_by_visible_text(value2)

    # 获取输入框的值
    def get_input_attribute(self, type, value1, value2):
        if type == "xpath":
            Value = self.driver.find_element_by_xpath(value1).get_attribute(value2)
            return Value
        elif type == "name":
            Value = self.driver.find_element_by_name(value1).get_attribute(value2)
            return Value
        elif type == "link_text":
            Value = self.driver.find_element_by_link_text(value1).get_attribute(value2)
            return Value
        elif type == "class_name":
            Value = self.driver.find_element_by_class_name(value1).get_attribute(value2)
            return Value
        elif type == "id":
            Value = self.driver.find_element_by_id(value1).get_attribute(value2)
            return Value
        elif type == "css_selector":
            Value = self.driver.find_element_by_css_selector(value1).get_attribute(value2)
            return Value

    # 获取下拉框的文本的值
    def get_droplist_text(self, type, value):
        if type == "xpath":
            text = self.driver.find_element_by_xpath(value).text
            return text
        elif type == "name":
            text = self.driver.find_element_by_name(value).text
            return text
        elif type == "link_text":
            text = self.driver.find_element_by_link_text(value).text
            return text
        elif type == "class_name":
            text = self.driver.find_element_by_class_name(value).text
            return text
        elif type == "id":
            text = self.driver.find_element_by_id(value).text
            return text

    # 显性等待时间
    def WebDriverWait(self, MaxTime, Mimtime, value):
        element = self.driver.find_element(By.ID, value)
        WebDriverWait(self.driver, MaxTime, Mimtime).until(EC.presence_of_element_located(element))

    # 鼠标移动点击
    def mouser_move_action(self, type, value):
        if type == "xpath":
            xm = self.driver.find_element_by_xpath(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "id":
            xm = self.driver.find_element_by_id(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "name":
            xm = self.driver.find_element_by_name(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "link_text":
            xm = self.driver.find_element_by_link_text(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).click()

    # 校验按钮是否为选中状态
    def check_button_is_selected(self, type, value):
        if type == "id":
            self.driver.find_element_by_id(value).is_selected()
        elif type == "xpath":
            self.driver.find_element_by_xpath(value).is_selected()
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).is_selected()
        elif type == "name":
            self.driver.find_element_by_name(value).is_selected()
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).is_selected()

    #封装元素等待（1、显示等待 2、隐式等待 3、time.sleep()）
    # 元素可见时，再进行后续操作
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located(param))

    #界面弹出框处理
    def alertHandle(self):
        # time.sleep(1)
        # # 等待alert弹出框可见
        # WebDriverWait(self.driver, 20).until(EC.alert_is_present())
        # 从html页面切换到alert弹框
        alert = self.driver.switch_to.alert
        # 获取alert的文本内容
        print(alert.text)
        # “确定”
        #alert.accept()
        #取消
        alert.dismiss()

    # 滚动条拖动到指定元素
    def srollBarToElement(self,value):
        webElement = self.driver.find_element_by_xpath(value)
        if webElement:
            self.driver.execute_script("arguments[0].scrollIntoView(false);", webElement)
        else:
            logger.error("元素查找失败")
