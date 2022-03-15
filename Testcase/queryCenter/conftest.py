import pytest
from pageObject.taskCenter import taskCenter

@pytest.fixture(scope="function",autouse = True)
def openQueryCenter(login):
    print("打开查询中心模块")
    driver = login[0]
    # 查询中心
    taskCenter(driver).queryCenter()
    yield login
    # return login


