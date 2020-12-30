#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/1 19:20
# @Author : Yulong Sun
# @Site : 
# @File : dataAnay.py
# @Software: PyCharm

import numpy as np
import xlrd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def updatecurrentVandS(currentV, currentS, action, double_dT=1, delaytime=0):
    """
    更新当前速度和距离，从列车动力学模型获取
    :param currentV:当前列车实际速度
    :param currentS:当前列车距离停车点的距离
    :param action:采取的挡位
    :return:采取档位后得到的新速度和距离
    """
    global acc, currentVt
    if action == 0:
        acc = 0
        currentVt = currentV

    elif action == 1:
        if 0 <= currentV <= 10:
            acc = 0.07875 + 0.003375 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 10 < currentV <= 160:
            acc = 0.1125
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 160 < currentV <= 240:
            acc = (0.1975 - 0.00053125 * currentV)
            currentVt = currentV - acc * (double_dT + delaytime)
        else:
            # 240<currentV<=350
            acc = (0.117142857 - 0.000196429 * currentV)
            currentVt = currentV - acc * (double_dT + delaytime)
    elif action == 2:
        if 0 <= currentV <= 10:
            acc = 0.1575 + 0.00675 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 10 < currentV <= 160:
            acc = 0.225
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 160 < currentV <= 240:
            acc = 0.395 - 0.0010625 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        else:
            # 240<currentV<=350
            acc = 0.234285714 - 0.0003928571416 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
    elif action == 3:
        if 0 <= currentV <= 10:
            acc = 0.23625 + 0.010125 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 10 < currentV <= 160:
            acc = 0.3375
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 160 < currentV <= 240:
            acc = 0.5925 - 0.00159375 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        else:
            # 240<currentV<=350
            acc = 0.351428571 - 0.0005892857125 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
    elif action == 4:
        if 0 <= currentV <= 10:
            acc = (0.315 + 0.0135 * currentV)
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 10 < currentV <= 160:
            acc = 0.45
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 160 < currentV <= 240:
            acc = 0.79 - 0.002125 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        else:
            # 240<currentV<=350
            acc = 0.468571429 - 0.000785714 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
    elif action == 5:
        if 0 <= currentV <= 10:
            acc = 0.371 + 0.02023328 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 10 < currentV <= 160:
            acc = 0.5733328
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 160 < currentV <= 240:
            acc = 1.02 - 0.00279167 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        else:
            # 240<currentV<=350
            acc = 0.585714285 - 0.0009821428541 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
    elif action == 6:
        if 0 <= currentV <= 5:
            acc = 0.515
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 5 <= currentV <= 20:
            acc = 0.435 + 0.0160 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 20 < currentV <= 160:
            acc = 0.755
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 160 < currentV <= 240:
            acc = 1.378 - 0.00389375 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        else:
            # 240<currentV<=350
            acc = 0.774857141992 - 0.0013806547583 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
    elif action == 7:
        if 0 <= currentV <= 5:
            acc = 0.5635
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 5 < currentV <= 20:
            acc = 0.483 + 0.0161 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 20 < currentV <= 160:
            acc = 0.805
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 160 < currentV <= 240:
            acc = 1.47 - 0.00415625 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
        else:
            # 240<currentV<=350
            acc = 0.8325 - 0.0015 * currentV
            currentVt = currentV - acc * (double_dT + delaytime)
    else:
        # 纯空气紧急制动action == 8
        if 0 <= currentV <= 250:
            acc = 0.98
            currentVt = currentV - acc * (double_dT + delaytime)
        elif 250 < currentV <= 300:
            acc = 0.75
            currentVt = currentV - acc * (double_dT + delaytime)
        else:
            # 300 < currentV <= 350
            acc = 0.40
            currentVt = currentV - 0.40 * (double_dT + delaytime)

    if action == 0:
        currentS = currentS - currentV * double_dT
    else:
        currentS = currentS + (currentVt ** 2 - currentV ** 2) / (2 * acc)

    # newresult = trac_new.trac_new_speed(currentV, int(float(action)), 10)
    # currentS = currentS - newresult[1]
    # currentV = newresult[0]

    return acc
print("-----------------------------actr-----------------------------")
workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为270_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
actr_dis, actr_xiansu, actr_actuv, actr_acc,actr_action = [], [], [], [],[]
for i in booksheet.col_values(0):
    actr_dis.append(round(i, 1))
for i in booksheet.col_values(1):
    actr_xiansu.append(round(i, 1))
for i in booksheet.col_values(2):
    actr_actuv.append(round(i, 1))
for i in booksheet.col_values(3):
    actr_action.append(round(i))
for i in booksheet.col_values(4):
    actr_acc.append(round(i,4))

print(actr_dis)
print(actr_xiansu)
print(actr_actuv)
print(actr_acc)
actrchongjilevel=0
for i in range(len(actr_acc)-1):
    actrchongjilevel += abs(actr_acc[i+1]-actr_acc[i])
print("ACTR冲击率：",actrchongjilevel)
print("ACTR最大加速度：",max(actr_acc))
print("ACTR平均加速度：",np.mean(actr_acc))

print("-----------------------------pid-----------------------------")
workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\result_pid.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
pid_dis, pid_xiansu, pid_actuv, pid_acc = [], [], [], []
for i in booksheet.col_values(0):
    pid_dis.append(round(i, 1))
for i in booksheet.col_values(1):
    pid_xiansu.append(round(i, 1))
for i in booksheet.col_values(2):
    pid_actuv.append(round(i, 1))
for i in booksheet.col_values(4):
    pid_acc.append(round(i, 4))
print(pid_dis)
print(pid_xiansu)
print(pid_actuv)
print(pid_acc)
pidchongjilevel=0
for i in range(len(pid_acc)-1):
    pidchongjilevel += abs(pid_acc[i+1]-pid_acc[i])
print("PID冲击率：",pidchongjilevel)
print("PID最大加速度：",max(pid_acc))
print("PID平均加速度：",np.mean(pid_acc))

print("-----------------------------driver-----------------------------")
workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\s-d1.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
driver_dis, driver_xiansu, driver_actuv, driver_action = [], [], [], []
for i in booksheet.col_values(4):
    driver_dis.append(round(i, 1))
for i in booksheet.col_values(1):
    driver_xiansu.append(round(i, 1))
for i in booksheet.col_values(0):
    driver_actuv.append(round(i, 1))
for i in booksheet.col_values(2):
    driver_action.append(round(i, 4))
print(driver_dis)
print(driver_xiansu)
print(driver_actuv)
print(driver_action)

action_acc=[]
for i in range(len(driver_action)):
    action_acc.append(updatecurrentVandS(driver_actuv[i], driver_dis[i], driver_action[i]))
driverchongjilevel=0
for i in range(len(action_acc)-1):
    driverchongjilevel += abs(action_acc[i+1]-action_acc[i])
print("司机冲击率：",driverchongjilevel)
print("司机最大加速度：",max(action_acc))
print("司机平均加速度：",np.mean(action_acc))

print("action_acc:",action_acc)
print("driver_action:",driver_action)
print("driver_actuv:",driver_actuv)
print("--------------------------------------------------")
print("actr_acc:",actr_acc)
print("actr_action:",actr_action)
print("actr_actuv:",actr_actuv)


print("-----------------------------driver-----------------------------")
workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\s-d1.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
speed, dis,limitressult = [], [], []

for i in booksheet.col_values(1):
    # print("iiiiiiiiiiii",i)
        speed.append(int(i))
for i in booksheet.col_values(4):
    dis.append(round(i, 1))

print("+++++++++++++++++++")
print(speed)
print(dis)
print(len(dis))
# for i in range(len(actr_dis)):
#     if actr_dis[i]>500:
#         speed.append(actr_dis[i])
#     else:
y=speed[len(speed):len(speed)-94:-1][::-1]
y=[60, 60, 60, 60, 60, 60, 60, 55, 55, 55, 55, 55, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 40, 45, 40, 40, 40, 40, 40, 40, 40, 40, 35, 35, 35, 35, 35, 35, 30, 30, 30, 30, 30, 30, 30, 30, 25, 25, 25, 25, 25, 25, 25, 25, 20, 20, 20, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 10, 15, 15, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
x=[494.7, 494.7, 494.7, 487.5, 480.2, 462.4, 448.4, 445.0, 428.0, 414.6, 398.1, 385.3, 378.9, 378.4, 372.7, 360.4, 351.4, 342.6, 334.0, 325.7, 317.5, 306.9, 304.3, 303.9, 301.8, 286.7, 281.8, 271.2, 269.9, 257.9, 255.6, 253.8, 248.9, 248.9, 248.9, 237.7, 233.4, 226.8, 216.2, 214.2, 206.0, 200.1, 200.1, 198.2, 196.2, 186.8, 179.5, 172.5, 165.6, 164.0, 152.6, 148.6, 148.0, 142.0, 135.0, 129.6, 127.0, 123.2, 113.5, 107.9, 100.4, 94.5, 88.9, 83.7, 82.1, 82.1, 77.5, 53.3, 50.4, 42.5, 37.9, 37.3, 36.7, 32.7, 32.1, 32.1, 31.6, 28.6, 28.6, 22.6, 22.6, 21.3, 15.6, 13.4, 12.1, 11.2, 4.5, 2.7, 2.5, 2.3, 1.0, 0.2, -0.0]

speed,dis=[],[]
# -----------------------------读取多种情形-----------------------------
for i in range(len(actr_dis)):
    if actr_dis[i]>500:
        dis.append(actr_dis[i])
        speed.append(actr_xiansu[i])
for i in range(len(y)):
    dis.append(x[i])
    speed.append(y[i])
for i in range(74,86):
    speed[i]=265
for i in range(304,307):
    speed[i]=130


print("-----------------------------读取多种情形-----------------------------")
workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为270_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为270_初始距离为9155,acc_初速度为270_初始距离为9155,actuv_初速度为270_初始距离为9155,dis_初速度为270_初始距离为9155,xiansu_初速度为270_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为270_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为270_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为270_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为270_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为270_初始距离为9155.append(round(i, 4))
print(acc_初速度为270_初始距离为9155)
print(action_初速度为270_初始距离为9155)
print(actuv_初速度为270_初始距离为9155)
print(xiansu_初速度为270_初始距离为9155)
print(dis_初速度为270_初始距离为9155)

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为268_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为268_初始距离为9155,acc_初速度为268_初始距离为9155,actuv_初速度为268_初始距离为9155,dis_初速度为268_初始距离为9155,xiansu_初速度为268_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为268_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为268_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为268_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为268_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为268_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为266_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为266_初始距离为9155,acc_初速度为266_初始距离为9155,actuv_初速度为266_初始距离为9155,dis_初速度为266_初始距离为9155,xiansu_初速度为266_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为266_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为266_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为266_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为266_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为266_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为264_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为264_初始距离为9155,acc_初速度为264_初始距离为9155,actuv_初速度为264_初始距离为9155,dis_初速度为264_初始距离为9155,xiansu_初速度为264_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为264_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为264_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为264_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为264_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为264_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为262_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为262_初始距离为9155,acc_初速度为262_初始距离为9155,actuv_初速度为262_初始距离为9155,dis_初速度为262_初始距离为9155,xiansu_初速度为262_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为262_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为262_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为262_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为262_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为262_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为270_初始距离为9100_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为270_初始距离为9100,acc_初速度为270_初始距离为9100,actuv_初速度为270_初始距离为9100,dis_初速度为270_初始距离为9100,xiansu_初速度为270_初始距离为9100,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为270_初始距离为9100.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为270_初始距离为9100.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为270_初始距离为9100.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为270_初始距离为9100.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为270_初始距离为9100.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为270_初始距离为9200_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为270_初始距离为9200,acc_初速度为270_初始距离为9200,actuv_初速度为270_初始距离为9200,dis_初速度为270_初始距离为9200,xiansu_初速度为270_初始距离为9200,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为270_初始距离为9200.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为270_初始距离为9200.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为270_初始距离为9200.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为270_初始距离为9200.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为270_初始距离为9200.append(round(i, 4))


workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为280_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为280_初始距离为9155,acc_初速度为280_初始距离为9155,actuv_初速度为280_初始距离为9155,dis_初速度为280_初始距离为9155,xiansu_初速度为280_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为280_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为280_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为280_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为280_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为280_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为278_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为278_初始距离为9155,acc_初速度为278_初始距离为9155,actuv_初速度为278_初始距离为9155,dis_初速度为278_初始距离为9155,xiansu_初速度为278_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为278_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为278_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为278_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为278_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为278_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为280_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为276_初始距离为9155,acc_初速度为276_初始距离为9155,actuv_初速度为276_初始距离为9155,dis_初速度为276_初始距离为9155,xiansu_初速度为276_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为276_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为276_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为276_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为276_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为276_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为280_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为274_初始距离为9155,acc_初速度为274_初始距离为9155,actuv_初速度为274_初始距离为9155,dis_初速度为274_初始距离为9155,xiansu_初速度为274_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为274_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为274_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为274_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为274_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为274_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为280_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为272_初始距离为9155,acc_初速度为272_初始距离为9155,actuv_初速度为272_初始距离为9155,dis_初速度为272_初始距离为9155,xiansu_初速度为272_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为272_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为272_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为272_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为272_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为272_初始距离为9155.append(round(i, 4))

workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\result\初速度为260_初始距离为9155.7_result_actr.xlsx')
booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
action_初速度为260_初始距离为9155,acc_初速度为260_初始距离为9155,actuv_初速度为260_初始距离为9155,dis_初速度为260_初始距离为9155,xiansu_初速度为260_初始距离为9155,=[],[],[],[],[]
for i in booksheet.col_values(0):
    dis_初速度为260_初始距离为9155.append(round(i, 3))
for i in booksheet.col_values(1):
    xiansu_初速度为260_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(2):
    actuv_初速度为260_初始距离为9155.append(round(i, 4))
for i in booksheet.col_values(3):
    action_初速度为260_初始距离为9155.append(round(i, 1))
for i in booksheet.col_values(4):
    acc_初速度为260_初始距离为9155.append(round(i, 4))



plt.figure(1)
# print("------------------------------不同情况下actr的输出速度对比图------------------------------")
# plt.axis([max(max(pid_dis),max(actr_dis)), -200, 0, max(max(pid_xiansu),max(actr_xiansu)) + 1])
# plt.plot(dis_初速度为280_初始距离为9155, actuv_初速度为280_初始距离为9155, linestyle="-", linewidth=1,
#      label='280_9155.7')
# plt.plot(dis_初速度为278_初始距离为9155, actuv_初速度为278_初始距离为9155, linestyle=":", linewidth=1,
#      label='278_9155.7')
# plt.plot(dis_初速度为276_初始距离为9155, actuv_初速度为276_初始距离为9155, linestyle="-.", linewidth=1,
#      label='276_9155.7')
# plt.plot(dis_初速度为274_初始距离为9155, actuv_初速度为274_初始距离为9155, linestyle="-", linewidth=1,
#      label='274_9155.7')
# plt.plot(dis_初速度为272_初始距离为9155, actuv_初速度为272_初始距离为9155, linestyle="-", linewidth=1,
#      label='272_9155.7')
# plt.plot(dis_初速度为270_初始距离为9200, actuv_初速度为270_初始距离为9200, linestyle="-", linewidth=1,
#      label='270_9200')
# plt.plot(dis_初速度为270_初始距离为9100, actuv_初速度为270_初始距离为9100, linestyle="dashed", linewidth=1,
#      label='270_9100')
# plt.plot(dis_初速度为270_初始距离为9155, actuv_初速度为270_初始距离为9155, linestyle="dashdot", linewidth=1,
#      label='270_9155.7')
# plt.plot(dis_初速度为268_初始距离为9155, actuv_初速度为268_初始距离为9155, linestyle="-", linewidth=1,
#      label='268_9155.7')
# plt.plot(dis_初速度为266_初始距离为9155, actuv_初速度为266_初始距离为9155, linestyle="dotted", linewidth=1,
#      label='266_9155.7')
# plt.plot(dis_初速度为264_初始距离为9155, actuv_初速度为264_初始距离为9155, linestyle=":", linewidth=1,
#      label='264_9155.7')
# plt.plot(dis_初速度为262_初始距离为9155, actuv_初速度为262_初始距离为9155, linestyle="-.", linewidth=1,
#      label='262_9155.7')
# plt.plot(dis_初速度为260_初始距离为9155, actuv_初速度为260_初始距离为9155, linestyle="--", linewidth=1,
#      label='260_9155.7')
# plt.plot(driver_dis, driver_actuv, linestyle="-", linewidth=1,
#      label='270_9155.7（人类高铁司机）')
# plt.plot(dis, speed, linestyle="solid", linewidth=1,
#      label='限制速度',color="red")
# plt.xlabel(u'距离（单位：m）')
# plt.ylabel(u'速度（单位：km/h）')
# plt.legend(loc=0)
# plt.savefig("../pyactrforstoptrain1/result/actr-pid-driver-velocity-more.png",dpi=1800)
# plt.show()
# print("------------------------------------------------------------")

# print("------------------------------actr、司机的输出速度对比图------------------------------")
# plt.axis([max(max(pid_dis),max(actr_dis)), -200, 0, max(max(pid_xiansu),max(actr_xiansu)) + 1])
# plt.plot(dis_初速度为270_初始距离为9155, actuv_初速度为270_初始距离为9155, linestyle="--", linewidth=1,
#      label='初速度为270_初始距离为9155')
# plt.plot(driver_dis, driver_actuv, linestyle="-", linewidth=1,
#      label='人类高铁司机驾驶速度')
# plt.legend()
# plt.savefig("../pyactrforstoptrain1/result/actr-driver-velocity-2.png")
# plt.show()
# print("------------------------------------------------------------")
#
#
#
#
#
#
# #
# # #
# # #
# #
# print("------------------------------actr、司机以及pid的输出速度对比图------------------------------")
# plt.axis([max(max(pid_dis),max(actr_dis)), -200, 0, max(max(pid_xiansu),max(actr_xiansu)) + 1])
# plt.plot(pid_dis, pid_actuv, linestyle="--", linewidth=1,
#      label='PID算法')
# plt.plot(actr_dis, actr_actuv, linestyle=":", linewidth=1,color='black',
#      label='本文算法')
# plt.plot(driver_dis, driver_actuv, linestyle="-.", linewidth=1,
#      label='人类高铁司机')
# plt.plot(dis, speed, linestyle="-", linewidth=1,
#      label='限制速度',color='red')
# plt.xlabel(u'距离（单位：m）')
# plt.ylabel(u'速度（单位：km/h）')
# plt.legend()
# plt.savefig("../pyactrforstoptrain1/result/actr-pid-driver-velocity.png",dpi=1800)
# plt.show()
# print("------------------------------------------------------------")
# #
# print()
# print("------------------------------actr、司机以及pid的输出加速度对比图------------------------------")
# plt.axis([max(max(pid_dis),max(actr_dis)), -200, 0, max(max(pid_acc),max(actr_acc))+0.05])
# plt.plot(pid_dis, pid_acc, linestyle="-.", linewidth=1,
#      label='PID算法')
# plt.plot(actr_dis, actr_acc, linestyle="--", linewidth=1,
#      label='本文算法')
# plt.plot(driver_dis, action_acc, linestyle="-", linewidth=1,
#      label='人类高铁司机')
# plt.xlabel(u'距离（单位：m）')
# plt.ylabel(u'输出制动减速度（单位：m/$\mathregular{s^2}$）')
# plt.legend()
# plt.savefig("../pyactrforstoptrain1/result/actr-pid-driver-acc.png",dpi=1800)
# plt.show()
# print("------------------------------------------------------------")
# #
# print("------------------------------actr和司机的输出加速度对比图------------------------------")
# plt.axis([max(max(actr_dis),max(driver_dis)), -200, 0, max(max(actr_acc),max(action_acc)) +0.1])
#
# plt.plot(actr_dis, actr_acc, linestyle="-", linewidth=1,
#      label='模型输出加速度')
# plt.plot(driver_dis, action_acc, linestyle="-", linewidth=1,
#      label='人类高铁司机输出加速度')
# plt.legend()
# plt.savefig("../pyactrforstoptrain1/result/actr-dirver-acc.png")
# plt.show()
# print("------------------------------------------------------------")
#
print("------------------------------actr和司机的输出挡位对比图------------------------------")
plt.axis([max(max(driver_dis),max(actr_dis)), -200, 0, max(max(driver_action),max(actr_action)) + 1])

# plt.xlabel="qwqwwq"
plt.plot(actr_dis, actr_action, linestyle=":", linewidth=1,color='red',
     label='本文算法')
plt.plot(driver_dis, driver_action, linestyle="-", linewidth=1,
     label='人类高铁司机')
plt.xlabel(u'距离（单位：m）')
plt.ylabel(u'制动级位')
plt.legend()
plt.savefig("../pyactrforstoptrain1/result/actr-driver-action.png",dpi=1800)
plt.show()
print("------------------------------------------------------------")