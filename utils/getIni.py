'''
    读取pytest.ini文件，根据addopts行中环境信息（--env值）来传递给对应测试用例，测试用例@pytest.mark.skipif()装饰器根据此值来
    判断该测试用例是否适用目前运行环境。
    如:批量抵押业务，无锡环境没有该流程，宜兴，泰州，宿迁有该流程。
'''

import os
iniFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'pytest.ini')

env = ['tztest','yxtest','sqtest','wxtest']
def getEnv():
    with open(iniFilePath, encoding='utf-8', mode='r') as f:
        data = f.readlines()    # 返回列表
    addopts_data = data[1].split()
    for i in range(len(addopts_data)):
        if addopts_data[i] in env:
            return addopts_data[i]
