#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/19 10:44
# @Author : Yulong Sun
# @Site : 
# @File : pidtest.py
# @Software: PyCharm
import xlrd

workbook = xlrd.open_workbook(r'..\s-d1.xlsx')
# workbook = xlrd.open_workbook(r'C:\Users\syl\Desktop\trainforactr\myDriveForChunk.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
carspeed, dangwei, tuijianspeed, dis_juli = [], [], [], []
for i in booksheet.col_values(2):
    # print("iiiiiiiiiiii",i)
    dangwei.append(int(i))
for i in booksheet.col_values(0):
    carspeed.append(round(i, 1))
for i in booksheet.col_values(1):
    tuijianspeed.append(round(i, 1))
for i in booksheet.col_values(4):
    dis_juli.append(round(i, 1))
print(dangwei)
count=0
for i in range(len(dangwei)-1):

    if dangwei[i]!= dangwei[i+1]:
       count +=1
       print(dangwei[i-1:i+3])
print("调整次数！",count)

output = 0

action = 0.0
print(round(abs(output), 2))
for i in range(51):
    print(round(0.1 * i, 2), round(0.1 * i + 0.1, 2))
    if 0.1 * i <= abs(output) < 0.1 * i + 0.1:
        print("actionss",action)
        action = round(0.1 * i, 2)
    else:
        action = 6

print(action)
print(0.0<=abs(0),abs(0)<=0.1)