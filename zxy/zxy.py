#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/6 16:00
# @Author : Yulong Sun
# @Site : 
# @File : zxy.py
# @Software: PyCharm

import xlrd
workbook = xlrd.open_workbook(r'五维分析.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
costLevel, timeLevel, xinxiaoLevel,ways,waysName =[], [], [],[],[]
data=[]
data2=[]
level={"高":4,"较高":3,"中等":2,"较低":1,"低":0,"成本等级（低代表不好）":7,"时间等级（低代表不好）":8,"信效度等级":9}
dataindex=[]
for i in booksheet.col_values(2):
    costLevel.append(level.get(i))
for i in booksheet.col_values(5):
    timeLevel.append(level.get(i))
for i in booksheet.col_values(6):
    xinxiaoLevel.append(level.get(i))
for i in booksheet.col_values(4):
    ways.append(i)
for i in booksheet.col_values(1):
    waysName.append(i)
print(costLevel)
print(timeLevel)
print(xinxiaoLevel)
print(ways)
print(waysName)
result=[]
def findWays(firstName=costLevel,secondName=timeLevel,thirdName=ways,way="数据收集法"):
    for i in range(len(firstName)):
        result.append([firstName[i], secondName[i], thirdName[i], ways[i]])
    print(result[0])

print("--------------------")
findWays()
print("@@@@@:",)
print("--------------------")






for i in range(len(costLevel)):
    result.append([costLevel[i],timeLevel[i],ways[i],xinxiaoLevel[i]])
print("!!!!1",result[0])

for i in range(len(result)):
    if result[i][2]=="数据收集法":
        data.append([result[i][0],result[i][1],result[i][3]])
print("未排序的data：",data)
# 按照成本、时间、信效度的顺序排序并找出相应的方法
sorted(data,key=(lambda x:x[0]),reverse=True)

# 找到最大索引对应的数组
for i in range(len(data)):
    if data[i][0]==sorted(data,key=(lambda x:x[0]),reverse=True)[0][0]:
        dataindex.append(i)
print("最大数对应的索引：",dataindex)
dict={}
for i,j in enumerate(data):
    dict.setdefault(i,j)
print("dict",dict)

# 找到下个指标大小的数组
for i in dataindex:
    data2.append(data[i])
# 继续排序
data2=sorted(data2,key=(lambda x:x[1]),reverse=True)
print("data2",data2)

data2index=[]
for i in range(len(data2)):
    if data2[i][1]==data2[0][1]:
        data2index.append(i)
print("data2index:",data2index)

# 找到第三个指标对应的数组
data3=[]
for i in data2index:
    data3.append(data2[i])
print("data3",data3)
# 继续排序
data3=sorted(data3,key=(lambda x:x[2]),reverse=True)
print("data3:",data3)
data3index=[]
for i in range(len(data3)):
    if data3[i][2]==data3[0][2]:
        data3index.append(i)
print("data3index:",data3index)
# 输出结果
resultIndex=[]
for i in data3index:
    resultIndex.append(data3[i])
    print("选中的方法名字：", waysName[i])

print(resultIndex)
for i in resultIndex:
    print("对应的索引：",data.index(i))




