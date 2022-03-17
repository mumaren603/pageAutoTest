import pytest
from Common.ToolsForOpertion import WebTools
from pageObject.taskCenter import taskCenter

@pytest.fixture(scope="function",autouse = True)
def openQueryCenter(login):
    '''
    :param login: 装饰器 调取登录方法（login(fixture)-->conftest）
    :return: driver对象和数据库配置信息
    :action: 模块下每个用例执行前需打开查询中心模块，执行后关闭查询中心
    '''
    print("打开查询中心模块")
    driver = login[0]
    # 查询中心
    taskCenter(driver).queryCenter()
    yield login
    WebTools(driver).switch_back_iframe()
    WebTools(driver).mouse_click('xpath', "//a[@xid='closeFuncBtn']")


