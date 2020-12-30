#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 18:24
# @Author : Yulong Sun
# @Site : 
# @File : stoptrain.py
# @Software: PyCharm
import pyactr as actr
import xlrd
from simpy.core import EmptySchedule
from pytracal import trac_new
import matplotlib.pyplot as plt
from PID import test_pid, PIDcontrol
import numpy as np
import pandas as pd



class actrstopmodel:
    def updatecurrentVandS(self, currentV, currentS, action, double_dT=1, delaytime=0):
        """
        更新当前速度和距离，从列车动力学模型获取
        :param currentV:当前列车实际速度
        :param currentS:当前列车距离停车点的距离
        :param action:采取的挡位
        :return:采取档位后得到的新速度和距离
        """
        global acc, currentVt
        if action == 0:
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
        VandS = [currentVt, currentS]
        return VandS

    def updatenextVandS(self, currentV, currentS):
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

        # ----------------------------2020/8/23-----------------------------------------------------------
        nextv = 0.042816923306331967 * (currentS ** 1) - 1.4556065943953415e-06 * (currentS ** 2)
        # ---------------------------------2020/8/23------------------------------------------------------
        # nextv1=[i for i in reversed(range(0,300,5))]
        # for i in range(1,61):
        #     if currentS<9155.7/i and  currentS>=9155.7/(i+1):
        #         nextv=nextv1[i-1]

        nexts = currentS
        # print("@@@@@@@@@@@@@@@@22", nextv)
        return nextv, nexts

    def actrsim(self, currentv,currentd,stopchangeflag=True):
        global action
        actr.chunktype("stoptrain_goal", "state")
        actr.chunktype("stopfortrain", "action curv curd")
        stoptrain = actr.ACTRModel(subsymbolic=True,
                                   activation_trace=True,
                                   retrieval_threshold=-88000,
                                   partial_matching=True,
                                   optimized_learning=True,
                                   production_compilation=True,
                                   motor_prepared=True,
                                   buffer_spreading_activation={"imaginal": 1},
                                   strength_of_association=1,
                                   decay=0.5,
                                   rule_firing=0.05,
                                   spreading_activation_restricted=True,
                                   association_only_from_chunks=False,
                                   mismatch_penalty=1,
                                   utility_learning=True,
                                   latency_factor=0.5,
                                   latency_exponent=0.5
                                   )
        dm = stoptrain.decmem
        g = stoptrain.goal
        stoptrain.retrieval.finst = 10
        imaginal = stoptrain.set_goal(name="imaginal", delay=0.2)

        # 档位信息
        judgestoptrain = stoptrain.set_goal("judgestoptrain")
        retriveaction = stoptrain.set_goal("retriveaction")
        # 初始化陈述性记忆中的经验
        dmchunk = []
        # dmchunk.append([1,25,238])
        dmchunk.append([1,15,80])
        dmchunk.append([1,1,80])
        # dmchunk.append([1,10,47])
        dmchunk.append([1,9,36.9])
        dmchunk.append([1,8,29.2])
        dmchunk.append([1,7,22.9])
        # dmchunk.append([1,6,16.7])
        # dmchunk.append([1,5,11.6])
        # dmchunk.append([1,4,7.6])
        # dmchunk.append([1,3,4.2])
        # dmchunk.append([1,2,1.9])
        # dmchunk.append([1,0.9,0.4])
        dmchunk.append([1,0.5,0.2])
        dmchunk.append([1,0,0])
        for i in dmchunk:
            # print("dmchunk", i[0])
            dm.add(actr.chunkstring(string="""
                isa stopfortrain
                action '""" + str(i[0]) + """'
                curv '""" + str(i[1]) + """'
                curd '""" + str(i[2]) + """'
            """))
        print("陈述性记忆：",dm)
        g.add(actr.chunkstring(string="""
                    isa stoptrain_goal
                    state start
                """))
        # 映像模块中添加初始记忆
        imaginal.add(actr.chunkstring(string="""
                    isa stopfortrain
                    curv '""" + str(currentv) + """'
                    curd '""" + str(currentd) + """'
                """))
        print("imaginal:", imaginal)

        stoptrain.productionstring(name="开始驾驶", string="""
                    =g>
                    isa stoptrain_goal
                    state start
                    =imaginal>
                    isa stopfortrain
                    curv =cv
                    curd =cd
                    ==>
                    =g>
                    isa stoptrain_goal
                    state startretrive
                    +retrieval>
                    isa stopfortrain
                    curv =cv
                    curd =cd
                """)
        stoptrain.productionstring(name="回忆成功", string="""
                    =g>
                    isa stoptrain_goal
                    state startretrive
                    =retrieval>
                    isa stopfortrain
                    action =a
                    ==>
                    =g>
                    isa stoptrain_goal
                    state doaction
                """, reward=10)
        stoptrain.productionstring(name="加大制动", string="""
                    =g>
                    isa stoptrain_goal
                    state doaction
                    =judgestoptrain>
                    isa Judgestoptrain
                    changeSpeed add
                    ?manual>
                    state   free
                    ==>
                    +manual>
                    isa     _manual
                    cmd     'press_key'
                    key     2
                    ~g>
                    ~retrieval>
                """)
        stoptrain.productionstring(name="撂1级闸", string="""
                    =g>
                    isa stoptrain_goal
                    state doaction
                    =judgestoptrain>
                    isa Judgestoptrain
                    changeSpeed keep
                    ?manual>
                    state   free
                    ==>
                    +manual>
                    isa     _manual
                    cmd     'press_key'
                    key     1
                    ~g>
                    ~retrieval>
                """)
        stoptrain.productionstring(name="释放制动", string="""
                    =g>
                    isa stoptrain_goal
                    state doaction
                    =judgestoptrain>
                    isa Judgestoptrain
                    changeSpeed 0
                    ?manual>
                    state   free
                    ==>
                    +manual>
                    isa     _manual
                    cmd     'press_key'
                    key     0
                    ~g>
                    ~retrieval>
                """)

        stoptrain_sim = stoptrain.simulation()

        while True:
            try:
                stoptrain_sim.step()
            except EmptySchedule:
                break
            #①判断速度是否大于0
            if stoptrain.goals['imaginal'] and float(stoptrain.goals['imaginal'].copy().pop()[1][1].__repr__()) > 0:
                imaginalcopy = stoptrain.goals['imaginal'].copy().pop()
                if stoptrain.retrieval:
                    # ②如果回忆成功，观察回忆的知识块的内容与实际速度的出入点，进行调整档位
                    retrievalcopy = stoptrain.retrieval.copy().pop()
                    # 实际速度和制动速度与经验值的差异
                    diffFordisshijiAndchunk = float(imaginalcopy[1][1].__repr__()) - float(retrievalcopy[1][1].__repr__())
                    diffForVshijiAndchunk = float(imaginalcopy[2][1].__repr__()) - float(retrievalcopy[2][1].__repr__())
                    print("实际速度与实际距离和知识块速度的差值：", diffForVshijiAndchunk, diffFordisshijiAndchunk)
                    action = int(float(retrievalcopy[0][1].__repr__()))
                    if float(imaginalcopy[2][1].__repr__()) <= 9:
                        if stopchangeflag:
                            print("---------------------------")
                            # 判断是否达到预期目标，若是就直接撂闸
                            if (diffForVshijiAndchunk< 0 and diffFordisshijiAndchunk >=0) or (diffForVshijiAndchunk == 0 and diffFordisshijiAndchunk >0) :
                                # 如果实际距离>知识块距离(未超过限速),则释放制动
                                stoptrain.goals["judgestoptrain"].add(
                                    actr.chunkstring(string="""isa Judgestoptrain
                                                               changeSpeed 0
                                                               """))
                            elif (diffFordisshijiAndchunk == 0 and diffForVshijiAndchunk == 0) :
                                stoptrain.goals["judgestoptrain"].add(
                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                changeSpeed keep 
                                                                """))
                                stopchangeflag=False
                            else:
                                stoptrain.goals["judgestoptrain"].add(
                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                changeSpeed add 
                                                                """))
                        else:
                            print("撂闸")
                            stoptrain.goals["judgestoptrain"].add(
                                actr.chunkstring(string="""isa Judgestoptrain
                                                           changeSpeed keep """))
            if stoptrain_sim.current_event[2][:-1] == 'KEY PRESSED: ':
                print("当前按键档位为：", stoptrain_sim.current_event[2][-1])
                action = int(stoptrain_sim.current_event[2][-1])
        desitime=stoptrain_sim.show_time()

        print("最终action:", action)
        print("运行时间：", desitime)
        return action,desitime,stopchangeflag

if __name__ == "__main__":

    global stopchangeflag
    stopchangeflag = True
    a1 = actrstopmodel()
    alltime=0
    count=0
    currentSforplt, currentVforplt, actionforplt = [], [], []
    currentV, currentS, action = 15,98.5, 1
    while currentV>0:
        updatecurVandS = a1.updatecurrentVandS(float(currentV * 1000 / 3600), float(currentS), action=1,
                                               double_dT=1)
        currentV = updatecurVandS[0] * 3600 / 1000
        currentS = updatecurVandS[1]
    print("运行总时间：", alltime)
    print("调整总次数：", count)
    print("停车距离：", currentS)
    print("停车速度：", currentV)



    # while currentV > 0:
    #     print("++++++++++++++++++++++++++++++第{}次++++++++++++++++++++++++++++++".format(count))
    #     action,desitime,stopchangeflag = a1.actrsim(currentv=round(currentV, 1), currentd=round(currentS, 1),stopchangeflag=stopchangeflag)
    #     print("主函数中的挡位",action)
    #     updatecurVandS = a1.updatecurrentVandS(float(currentV * 1000 / 3600), float(currentS), action,double_dT=desitime)
    #     currentV = updatecurVandS[0] * 3600 / 1000
    #     currentS = updatecurVandS[1]
    #     print("当前速度和当前距离：",currentV,currentS)
    #     alltime += desitime
    #     count +=1
    # print("运行总时间：", alltime)
    # print("调整总次数：", count)
    # print("停车距离：", currentS)
    # print("停车速度：", currentV)







































