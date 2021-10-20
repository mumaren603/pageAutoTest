import pytest
from selenium import webdriver
from Common.CommonFunc import WebTools
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from Common.logFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.fixture(scope="module")
def login(request,getConfValue):
    logger.debug("yaml中读取配置内容：%s" % getConfValue)

    driver_path = getConfValue.get('envinfo').get('browserDriver', None)
    logger.debug("浏览器驱动路径：%s" % driver_path)

    login_url = getConfValue.get('envinfo').get('url', None)
    logger.debug("url路径：%s" % login_url)

    login_user = getConfValue.get('envinfo').get('loginUser', None)
    logger.debug("登录用户信息：%s" % login_user)

    db_info = getConfValue.get('envinfo').get('db',None)
    logger.debug("<--------读取初始化配置数据end-------->")

    if driver_path and login_url and login_user:
        driver = webdriver.Chrome(executable_path=driver_path)
        WebTools(driver).set_browser(login_url)
        #登录
        WebTools(driver).check_element_is_exists('xpath', "//div[contains(@id,'_btnlogin')]")
        WebTools(driver).input_clear('xpath', "//input[contains(@id,'_name')]")
        WebTools(driver).input_clear('xpath', "//input[contains(@id,'_password')]")
        WebTools(driver).input_content('xpath', "//input[contains(@id,'_name')]", login_user.get('user'))
        WebTools(driver).input_content('xpath', "//input[contains(@id,'_password')]", login_user.get('passwd'))
        WebTools(driver).mouse_click('xpath', "//div[contains(@id,'_btnlogin')]")
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'办件中心')]")))
            yield driver ,db_info
        except NoSuchElementException:
            logger.error('NoSuchElementException')
            raise
        except Exception as e:
            logger.error('登录异常：',e)
            raise
    else:
        logger.error("全局登录信息缺失，请检查yaml配置文件。")

