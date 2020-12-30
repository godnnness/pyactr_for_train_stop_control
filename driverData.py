#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/18 17:34
# @Author : Yulong Sun
# @Site : 
# @File : driverData.py
# @Software: PyCharm
"""
这段代码的主要功能是：
"""
import xlrd
import matplotlib.pyplot as plt

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\s-d1.xlsx')
# workbook = xlrd.open_workbook(r'C:\Users\syl\Desktop\trainforactr\myDriveForChunk.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
dangwei,distance,actspeed,limitspeed= [], [],[], []
for i in booksheet.col_values(4):
    # print("iiiiiiiiiiii",i)
    distance.append(int(i))
for i in booksheet.col_values(2):
    dangwei.append(round(i, 1))
for i in booksheet.col_values(0):
    # print("iiiiiiiiiiii",i)
    actspeed.append(int(i))
for i in booksheet.col_values(1):
    limitspeed.append(round(i, 1))

plt.figure(1)
plt.subplot(211)
plt.axis([max(distance), -200, 0, max(limitspeed) + 1])

plt.plot(distance, actspeed, linestyle="-", linewidth=1,
         label='trainspeed')
plt.plot(distance, limitspeed, linestyle="-", linewidth=1,
         label='speed limit')
plt.legend()

plt.subplot(212)
plt.axis([max(distance), -200, 0, max(dangwei) + 1])
plt.plot(distance, dangwei, linestyle="-", linewidth=1,
         label='acc')
plt.legend()
plt.savefig(r"../pyactrforstoptrain1/result/driver.png")
plt.show()
