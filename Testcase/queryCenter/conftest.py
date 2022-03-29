import pytest
from Common.ToolsForOpertion import WebTools
from pageObject.taskCenter import taskCenter
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.fixture(scope="function")
def openQueryCenter(login):
    '''
    :param login: 装饰器 调取登录方法（login(fixture)-->conftest）
    :return: driver对象
    :action: 模块下每个用例执行前需打开查询中心模块，执行后关闭查询中心
    '''
    driver = login

    logger.debug("打开查询中心模块")
    # 查询中心
    taskCenter(driver).queryCenter()
    yield driver
    logger.debug("关闭查询中心模块")
    WebTools(driver).switch_back_iframe()
    WebTools(driver).mouse_click('xpath', "//a[@xid='closeFuncBtn']")



