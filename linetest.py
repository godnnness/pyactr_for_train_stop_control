#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/12 19:46
# @Author : Yulong Sun
# @Site : 
# @File : linetest.py
# @Software: PyCharm
import xlrd
import matplotlib.pyplot as plt
def updatenextVandS(currentS):
    """
    知道当前时刻的速度和距离，得到推荐速度、推荐距离
    优化曲线为当前距离和速度的一个六次曲线
    y = -2E-17x6 + 1E-13x5 - 3E-10x4 + 3E-07x3 - 0.0001x2 + 0.0259x

    :param currentV:
    :param currentS:
    :return:
    y = -1E-11x5 + 2E-08x4 - 2E-05x3 + 0.0042x2 - 0.5659x + 102.67
    """

    global nextv
    workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\s-d1.xlsx')
    booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
    dis, limitspeed = [], []
    for i in booksheet.col_values(4):
        # print("iiiiiiiiiiii",i)
        dis.append(int(i))
    for i in booksheet.col_values(1):
        limitspeed.append(round(i, 1))
    if currentS > 1720.2:
        for i in range(0, len(dis), 5):
            if i < len(dis) - 5:
                # print("speed[i+1],speed[i]: ",speed[i+10],speed[i])
                left = dis[i + 5]
                right = dis[i]
            else:
                # print("speed[i+1],speed[i]: ", speed[i])
                left = dis[-1]
                right = dis[i]
            # print(left,right)
            if left < currentS <= right:
                print(left, right)
                print(limitspeed[i])
                nextv = limitspeed[i]
            if currentS >= 9155.7:
                nextv = 300
    else:
        nextv = 0.122816923306331967 * (currentS ** 1) - 0.1056065943953415e-06 * (currentS ** 2)
    return nextv
nextvvv=[]
sss=[]
for i in reversed(range(1720)):
    nextvvv.append(updatenextVandS(currentS=i))
    sss.append(i)
plt.figure(1)
print("------------------------------不同情况下actr的输出速度对比图------------------------------")
plt.axis([max(sss), -200, 0, max(nextvvv) + 1])
plt.plot(sss, nextvvv, linestyle="-", linewidth=1,
     label='初速度为270_初始距离为9200')
plt.legend()
plt.show()