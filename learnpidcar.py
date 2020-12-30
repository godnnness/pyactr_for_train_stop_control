# /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import time

import pyactr as actr
import xlrd
import xlwt
from simpy.core import EmptySchedule
from pytracal import trac_new
import matplotlib.pyplot as plt
from PID import test_pid, PIDcontrol
import numpy as np
import pandas as pd
import openpyxl
import PID

# kp=1.15, ki=0.1, kd=10,基于GA优化模糊PID控制的ATO算法研究得到系统（列车模型）参数是0.4
# kp=19.12, ki=3.23, kd=4.14
# kp=10, ki=0, kd=0
def pidcontrol(kp=25.12, ki=4.23, kd=0.1, current_level=0.0, setLevel=0.0):
    """
    根据当前速度和推荐速度返回一个挡位值
    :param current_level:
    :param setLevel:
    :return:
    """

    # 优化曲线，理想制动为0.10015037593985067
    # y = 6.869398496240324 * (currentV ** 1) + 0.10015037593985067 * (currentV ** 2)
    global action
    stopTrainInPID1 = PIDcontrol.stopTrainInPID(kp, ki, kd,windup_guard=0.09)
    stopTrainInPID1.clear()
    stopTrainInPID1.SetLevel = setLevel
    stopTrainInPID1.update(current_level)
    output = stopTrainInPID1.output
    print("output:",abs(output))
    # 挡位与输出对应的关系
    for i in range(51):
        # print(round(0.1 * i, 2), round(0.1 * i + 0.1, 2))
        left=0.1 * i
        right= 0.1 * i + 0.1
        if left <= abs(output) < right:
            action = round(0.1 * i, 2)
            break
        else:
            action = 6
    return action
def accTOspeed(currentV,action):
    if action==0:
        acc=0
    elif action==1:
        if 0<=currentV<=10:
            acc=0.07875+0.003375*currentV
        elif 10<currentV<=160:
            acc = 0.1125
        elif 160<currentV<=240:
            acc = (0.1975-0.00053125*currentV)
        else:
            #240<currentV<=350
            acc = (0.117142857 - 0.000196429 * currentV)
    elif action==2:
        if 0<=currentV<=10:
            acc=0.1575 + 0.00675*currentV
        elif 10<currentV<=160:
            acc = 0.225
        elif 160<currentV<=240:
            acc = 0.395 - 0.0010625*currentV
        else:
            #240<currentV<=350
            acc = 0.234285714 - 0.0003928571416 * currentV
    elif action==3:
        if 0<=currentV<=10:
            acc=0.23625 + 0.010125*currentV
        elif 10<currentV<=160:
            acc = 0.3375
        elif 160<currentV<=240:
            acc = 0.5925 - 0.00159375 *currentV
        else:
            #240<currentV<=350
            acc = 0.351428571 - 0.0005892857125 * currentV
    elif action==4:
        if 0<=currentV<=10:
            acc=(0.315+0.0135*currentV)
        elif 10<currentV<=160:
            acc=0.45
        elif 160<currentV<=240:
            acc=0.79-0.002125*currentV
        else:
            #240<currentV<=350
            acc=0.468571429 - 0.000785714 * currentV
    elif action==5:
        if 0<=currentV<=10:
            acc=0.371 + 0.02023328*currentV
        elif 10<currentV<=160:
            acc=0.5733328
        elif 160<currentV<=240:
            acc=1.02 - 0.00279167 * currentV
        else:
            #240<currentV<=350
            acc=0.585714285 - 0.0009821428541 * currentV
    elif action==6:
        if 0<=currentV<=5:
            acc=0.515
        elif 5<=currentV<=20:
            acc=0.435+0.0160 * currentV
        elif 20<currentV<=160:
            acc=0.755
        elif 160<currentV<=240:
            acc=1.378 - 0.00389375 * currentV
        else:
            #240<currentV<=350
            acc=0.774857141992 - 0.0013806547583 * currentV
    elif action==7:
        if 0 <= currentV <= 5:
            acc=0.5635
        elif 5 < currentV <= 20:
            acc=0.483 + 0.0161 * currentV
        elif 20 < currentV <= 160:
            acc=0.805
        elif 160 < currentV <= 240:
            acc=1.47-0.00415625* currentV
        else:
            # 240<currentV<=350
            acc = 0.8325-0.0015 * currentV
    else:
        #纯空气紧急制动action == 8
        if 0 <= currentV <= 250:
            acc = 0.98
        elif 250 < currentV <= 300:
            acc = 0.75
        else:
            # 300 < currentV <= 350
            acc = 0.40
    return acc
def updatecurrentVandS(currentV, currentS, action, double_dT=0.1,delaytime=0):
    """
    更新当前速度和距离，从列车动力学模型获取
    :param currentV:当前列车实际速度 km/h
    :param currentS:当前列车距离停车点的距离
    :param action:采取的挡位
    :return:采取档位后得到的新速度和距离
    若按照级位控制模式，+1级/s,+0.1级/s,初始级位如何选择
    加速度的单位是m/s2
    """

    global acc, currentVt, acc1, acc2
    print("开始的挡位：",action)
    if action==0.0 or action==1.0 or action==2.0 or action==3.0 or action==4.0 or action==5.0 or action==6.0 or action==7.0 or action==8.0:
        acc = accTOspeed(currentV,action)
        print("整级挡位：",acc)
    elif 0<action<1:
        acc1=accTOspeed(currentV,1)
        acc2=accTOspeed(currentV,0)
        acc=(acc1-acc2)/10 * ((action-0)/0.1)+acc2
        print("0.*对应的挡位:",acc,acc1,acc2)


    elif 1<action<2:
        acc1=accTOspeed(currentV,2)
        acc2=accTOspeed(currentV,1)
        acc=(acc1-acc2)/10 * ((action-1)/0.1)+acc2
        print("1.*对应的挡位:",acc,acc1,acc2)

    elif 2<action<3:
        acc1=accTOspeed(currentV,3)
        acc2=accTOspeed(currentV,2)
        acc=(acc1-acc2)/10 * ((action-2)/0.1)+acc2
        print("2.*对应的挡位:",acc,acc1,acc2)

    elif 3<action<4:
        acc1=accTOspeed(currentV,4)
        acc2=accTOspeed(currentV,3)
        acc=(acc1-acc2)/10 * ((action-3)/0.1)+acc2
        print("3.*对应的挡位:",acc,acc1,acc2)
    else:
        acc1=accTOspeed(currentV, 5)
        acc2=accTOspeed(currentV, 4)
        acc=(acc1-acc2)/10 * ((action-4)/0.1)+acc2
        print("4.*对应的挡位:",acc,acc1,acc2)

    print("加速度021：",acc)

    currentVt = currentV - acc * (double_dT + delaytime)
    print("末速度、初速度、加速度",currentVt, currentV,acc)


    if action==0:
        currentS = currentS - currentV * double_dT
    else:
        currentS = currentS + (currentVt *currentVt - currentV *currentV) / (2 * acc)
        # currentS=currentV*double_dT-0.5*acc*double_dT*double_dT
    print("距离", currentS)



    VandS = [currentVt, currentS,acc]
    return VandS


if __name__ == "__main__":
    print(75/0.3072856876,75/309,(9155.7-75*309)*2/(309*309))

    sys.stdout = open(r"..\pyactrforstoptrain1\result\pidcontrol.txt", "w")
    currentV, nexV, currentS, action = 270, 300, 9155.7, 3
    pidactionforplt,pidnextv, pidcurrentVforplt, pidcurrentsforplt,accforplt,timeforeach=[], [], [], [], [],[]
    pidcount=0
    speedChange=[currentV]
    timeSpeedChange = 0

    while round(currentV,2) > 0:
        print("-----------------------")
        pidcount=pidcount+1
        # 优化曲线

        # nextvpid = (75-0.3072856876*pidcount/10)*3.6
        # 0.4001165048543689 0.16740837088307708 100 209
        # 0.3449249779346866 0.14117131224553714 154 155
        # a_1, a_2, t_1, t_2
        if pidcount<=1540:
            nextvpid = (75 - 0.3449249779346866 * pidcount / 10) * 3.6
        else:
            nextvpid = (75 - 0.3449249779346866 * 154 - 0.14117131224553714 * (pidcount / 10-154)) * 3.6

        print("nextvpid:",nextvpid)

        # 限速曲线

        print("限速以及次数：",nextvpid,pidcount)
        action = pidcontrol(current_level=currentV, setLevel=nextvpid)
        print("当前挡位：", action)
        updatecurVandS = updatecurrentVandS(float(currentV * 1000 / 3600), float(currentS), action, double_dT=0.1, delaytime=0)

        print("实际速度:",updatecurVandS[0],updatecurVandS[0]*3.6)
        print("理想速度：",nextvpid)
        currentV = updatecurVandS[0] * 3.6
        currentS = updatecurVandS[1]
        if currentV != speedChange[-1]:
            timeSpeedChange +=1
        speedChange.append(currentV)

        pidactionforplt.append(action)
        pidcurrentVforplt.append(currentV)
        pidcurrentsforplt.append(currentS)
        pidnextv.append(nextvpid)
        accforplt.append(updatecurVandS[2])

    # print([pidactionforplt, pidcurrentVforplt, pidnextv, pidcurrentsforplt])
    A = np.array([pidactionforplt, pidcurrentVforplt, pidnextv, pidcurrentsforplt]).T
    data = pd.DataFrame(A)

    writer = pd.ExcelWriter(r"pidandactr/pid-control.xlsx")  # 写入Excel文件
    data.to_excel(writer,header=None,index=None)  # ‘page_1’是写入excel的sheet名
    writer.save()

    writer.close()
    print("pid完成并退出", pidcurrentsforplt[-1],pidcurrentVforplt[-1])
    print("pid控制次数和距离：", pidcount, pidcurrentsforplt[-1])
    print("pid调整次数：", timeSpeedChange)


    plt.figure(1)
    plt.subplot(121)
    plt.axis([max(pidcurrentsforplt), -200, 0, max(pidnextv) + 1])
    plt.plot(pidcurrentsforplt, pidnextv, linestyle="-", linewidth=1,
         label='pidnextv')
    plt.plot(pidcurrentsforplt, pidcurrentVforplt, linestyle="-", linewidth=1,
         label='pidcurrentVforplt')

    plt.legend()
    plt.subplot(122)
    plt.axis([max(pidcurrentsforplt), -200, 0, max(pidactionforplt)])
    plt.plot(pidcurrentsforplt, pidactionforplt, linestyle="-", linewidth=1,
         label='pidactionforplt')
    plt.legend()
    plt.savefig("../pyactrforstoptrain1/result/similfprpid.png")
    plt.show()
    # 将所有结果保存到一个result.xlsx文件中
    A = np.array(pidcurrentsforplt)
    B = np.array(pidnextv)
    C = np.array(pidcurrentVforplt)
    D = np.array(pidactionforplt)
    E = np.array(accforplt)
    data = pd.DataFrame(A)
    data_1 = pd.DataFrame(B)
    data_2 = pd.DataFrame(C)
    data_3 = pd.DataFrame(D)
    data_4 = pd.DataFrame(E)
    writer = pd.ExcelWriter('../pyactrforstoptrain1/result/result_pid.xlsx')  # 写入Excel文件
    data.to_excel(writer, 'PID', float_format='%.5f',header=False,index=False,startrow=0,startcol=0,)
    data_1.to_excel(writer, 'PID', float_format='%.5f',header=False,index=False,startrow=0,startcol=1,)
    data_2.to_excel(writer, 'PID', float_format='%.5f',header=False,index=False,startrow=0,startcol=2,)
    data_3.to_excel(writer, 'PID', float_format='%.5f',header=False,index=False,startrow=0,startcol=3,)
    data_4.to_excel(writer, 'PID', float_format='%.5f',header=False,index=False,startrow=0,startcol=4,)
    writer.save()
    writer.close()