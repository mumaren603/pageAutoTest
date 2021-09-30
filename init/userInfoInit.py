'''本模块用于生成用户出初始信息，如用户姓名、证件号码、手机号等'''
# -*- coding: utf-8 -*-
import random
from datetime import datetime


#电话号码(8位)
def generateTelnum():
    telNum = ''
    for i in range(8):
        generateCode = random.randint(0,9)
        telNum += str(generateCode)
    return telNum

#证件号码（护照）（10位）
def generateCertNum():
    certNum = ''
    for i in range(0,9):
        generateCode = random.randint(0,9)
        certNum += str(generateCode)
    return certNum


code_list = []
for i in range(65, 91):   # 对应从“A”到“Z”的ASCII码
    code_list.append(chr(i))
for i in range(97, 123): #对应从“a”到“z”的ASCII码
    code_list.append(chr(i))
#权利人姓名(10位)
def generateQLRName():
    randomNum = random.sample(code_list, 10)     # 从list中随机获取15个元素，作为一个片断返回
    userName = ''.join(randomNum)       # list to string
    userName = 'TestUser_'+userName
    return userName

def generateDYQLRName():
    randomNum = random.sample(code_list, 5)     # 从list中随机获取15个元素，作为一个片断返回
    userName = ''.join(randomNum)       # list to string
    userName = 'BANKOFCHINA_'+userName
    return userName

#用户居住地址（30位）
def generateAddr():
    randomNum = random.sample(code_list, 20)     # 从list中随机获取15个元素，作为一个片断返回
    userAddr = ''.join(randomNum)       # list to string
    userAddr = "TestAddr_"+userAddr
    return userAddr

#查封文件
def generateCfwj():
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    currentMonth = '0' + str(currentMonth) if len(str(currentMonth)) == 1 else str(currentMonth)
    currentDay = datetime.now().day
    currentDay = '0' + str(currentDay) if len(str(currentDay)) == 1 else str(currentDay)
    currentHour = datetime.now().hour
    currentHour = '0' + str(currentHour) if len(str(currentHour)) == 1 else str(currentHour)
    currentMinute = datetime.now().minute
    currentMinute = '0' + str(currentMinute) if len(str(currentMinute)) == 1 else str(currentMinute)
    cfwj = "（"+str(currentYear)+"）苏"+currentMonth+currentDay+"民初"+currentHour+currentMinute+"号"
    return cfwj


