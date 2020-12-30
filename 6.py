# /usr/bin/env python
# -*- coding: UTF-8 -*-

import pyactr as actr
import xlrd
from simpy.core import EmptySchedule
from pytracal import trac_new
import matplotlib.pyplot as plt
from PID import test_pid, PIDcontrol
import numpy as np
import pandas as pd

import sys

class actrmodel:

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
            acc=0
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

        print("当前挡位{0:}对应的加速度{1:}".format(action,acc))

        # newresult = trac_new.trac_new_speed(currentV, int(float(action)), 10)
        # currentS = currentS - newresult[1]
        # currentV = newresult[0]
        VandS = [currentVt, currentS,acc]
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
        workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\s-d1.xlsx')
        booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
        dis, limitspeed = [], []
        for i in booksheet.col_values(4):
            # print("iiiiiiiiiiii",i)
            dis.append(int(i))
        for i in booksheet.col_values(1):
            limitspeed.append(round(i, 1))
        if currentS > 500:
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
            nextv = 0.122816923306331967 * (currentS ** 1) - 0.5056065943953415e-06 * (currentS ** 2)

        # ----------------------------2020/8/23-----------------------------------------------------------
        # if currentV>200:
        #     nextv=270
        # elif currentV>170:
        #     nextv=215
        # elif currentV>131:
        #     nextv=170
        # elif currentV>113:
        #     nextv=140
        # elif currentV>86:
        #     nextv=115
        # elif currentV>56:
        #     nextv=65
        # elif currentV>38:
        #     nextv=50
        # else:
        #     nextv = 0.042816923306331967 * (currentS ** 1) - 1.4556065943953415e-06 * (currentS ** 2)
        # ---------------------------------2020/8/23------------------------------------------------------

        nexts = currentS
        # print("@@@@@@@@@@@@@@@@22", nextv)
        return nextv, nexts

    def actrsim(self, currentv, nextv, currentd, stopSpeed=20, diffv=100):
        global action
        # currentV > 30结果最好
        if currentV>50:
            diffv=80
        else:
            diffv = 1
        actr.chunktype("stoptrain_goal", "state")
        actr.chunktype("stopfortrain", "action curv nexv curd")
        actr.chunktype("Retriveaction", "action")
        actr.chunktype("Judgestoptrain", "isnotchangespeed isnotuplimit diffimagVandretr diffimagDandretr hasaction ")

        stoptrain = actr.ACTRModel(subsymbolic=True,
                                   activation_trace=True,
                                   retrieval_threshold=-1000,
                                   partial_matching=True,
                                   optimized_learning=True,
                                   production_compilation=True,
                                   motor_prepared=True,
                                   buffer_spreading_activation={"imaginal": 10},
                                   strength_of_association=1.0,#影响较大,1.1取值较好的兼顾了控制次数与时间的关系
                                   decay=0.5,
                                   rule_firing=0.0001,
                                   spreading_activation_restricted=True,
                                   association_only_from_chunks=False,
                                   mismatch_penalty=1,
                                   utility_learning=True,
                                   latency_factor=0.5,
                                   latency_exponent=0.5)
        dm = stoptrain.decmem
        g = stoptrain.goal
        stoptrain.retrieval.finst = 10
        imaginal = stoptrain.set_goal(name="imaginal", delay=0.2)
        # 一把辛酸泪，都与谁人说
        # 档位信息
        judgestoptrain = stoptrain.set_goal("judgestoptrain")
        retriveaction = stoptrain.set_goal("retriveaction")

        # 初始化陈述性记忆中的经验
        dmchunk = []
        with open("chunk.csv", "w") as f:
            workbook = xlrd.open_workbook(r'..\pyactrforstoptrain1\s-d1.xlsx')
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
            # print("dangwei:\n", dangwei)
            # print("carspeed:\n", carspeed)
            # print("tuijianspeed:\n", tuijianspeed)
            # print("dis_juli:\n", dis_juli)

            for i in range(len(dangwei)):
                # 初始化陈述性记忆
                dmchunk.append([dangwei[i], carspeed[i], tuijianspeed[i], dis_juli[i]])
            # 必须要去重，否则不利于计算激活值
            dmchunk = list(set([tuple(t) for t in dmchunk]))
            # print("dmchunk",dmchunk)
            for i in dmchunk:
                # print("dmchunk", i[0])

                dm.add(actr.chunkstring(string="""
                    isa stopfortrain
                    action '""" + str(i[0]) + """'
                    curv '""" + str(i[1]) + """'
                    nexv '""" + str(i[2]) + """'
                    curd '""" + str(i[3]) + """'
                """))


        g.add(actr.chunkstring(string="""
            isa stoptrain_goal
            state start
        """))
        stoptrain.goals["retriveaction"].add(actr.chunkstring(string="""
                    isa Retriveaction
                    action None
        """))

        imaginal.add(actr.chunkstring(string="""
            isa stopfortrain
            curv '""" + str(currentv) + """'
            nexv '""" + str(nextv) + """'
            curd '""" + str(currentd) + """'
        """))
        print("imaginal:", imaginal)

        stoptrain.productionstring(name="开始驾驶",string="""
            =g>
            isa stoptrain_goal
            state start
            =imaginal>
            isa stopfortrain
            curv =cv
            nexv =nv
            curd =cd
            ==>
            =g>
            isa stoptrain_goal
            state startretrive
            +retrieval>
            isa stopfortrain
            curv =cv
            nexv =nv
            curd =cd
        """)
        stoptrain.productionstring(name="回忆成功",string="""
            =g>
            isa stoptrain_goal
            state startretrive
            =retrieval>
            isa stopfortrain
            action =a
            ==>
            =retriveaction>
            isa Retriveaction
            action =a
            =g>
            isa stoptrain_goal
            state doaction
        """, reward=10)
        stoptrain.productionstring(name="如果实际距离<知识块距离,实际速度>=知识块速度,则采取制动(知识块无制动)", string="""
                    =g>
                    isa stoptrain_goal
                    state doaction
                    =judgestoptrain>
                    isa Judgestoptrain
                    isnotchangespeed yes
                    isnotuplimit mid
                    diffimagDandretr L
                    diffimagVandretr GE
                    hasaction None
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
        stoptrain.productionstring(name="如果实际距离<知识块距离,实际速度>=知识块速度,则采取制动(知识块有制动)", string="""
                            =g>
                            isa stoptrain_goal
                            state doaction
                            =retriveaction>
                            isa Retriveaction
                            action =a
                            =judgestoptrain>
                            isa Judgestoptrain
                            isnotchangespeed yes
                            isnotuplimit mid
                            diffimagDandretr L
                            diffimagVandretr GE
                            hasaction yes
                            ?manual>
                            state   free
                            ==>
                            +manual>
                            isa     _manual
                            cmd     'press_key'
                            key     =a
                            ~g>
                            ~retrieval>
                        """)
        stoptrain.productionstring(name="如果实际距离>知识块距离,则释放制动", string="""
                                    =g>
                                    isa stoptrain_goal
                                    state doaction
                                    =judgestoptrain>
                                    isa Judgestoptrain
                                    isnotchangespeed yes
                                    isnotuplimit mid
                                    diffimagDandretr G
                                    diffimagVandretr any
                                    hasaction None
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
        stoptrain.productionstring(name="如果实际距离==知识块距离且实际速度>知识块速度,则采取制动(知识块无制动)", string="""
                            =g>
                            isa stoptrain_goal
                            state doaction
                            =judgestoptrain>
                            isa Judgestoptrain
                            isnotchangespeed yes
                            isnotuplimit mid
                            diffimagDandretr E
                            diffimagVandretr G
                            hasaction None
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
        stoptrain.productionstring(name="如果实际距离==知识块距离,实际速度>知识块速度,则采取制动(知识块有制动)", string="""
                                    =g>
                                    isa stoptrain_goal
                                    state doaction
                                    =retriveaction>
                                    isa Retriveaction
                                    action =a
                                    =judgestoptrain>
                                    isa Judgestoptrain
                                    isnotchangespeed yes
                                    isnotuplimit mid
                                    diffimagDandretr E
                                    diffimagVandretr G
                                    hasaction yes
                                    ?manual>
                                    state   free
                                    ==>
                                    +manual>
                                    isa     _manual
                                    cmd     'press_key'
                                    key     =a
                                    ~g>
                                    ~retrieval>
                                """)
        stoptrain.productionstring(name="如果实际距离==知识块距离且实际速度==知识块速度,则按照原档位", string="""
                                            =g>
                                            isa stoptrain_goal
                                            state doaction
                                            =retriveaction>
                                            isa Retriveaction
                                            action =a
                                            =judgestoptrain>
                                            isa Judgestoptrain
                                            isnotchangespeed yes
                                            isnotuplimit mid
                                            diffimagDandretr E
                                            diffimagVandretr E
                                            hasaction None
                                            ?manual>
                                            state   free
                                            ==>
                                            +manual>
                                            isa     _manual
                                            cmd     'press_key'
                                            key     =a
                                            ~g>
                                            ~retrieval>
                                        """)
        stoptrain.productionstring(name="如果实际距离==知识块距离且实际速度<知识块速度,则释放制动", string="""
                                    =g>
                                    isa stoptrain_goal
                                    state doaction
                                    =judgestoptrain>
                                    isa Judgestoptrain
                                    isnotchangespeed yes
                                    isnotuplimit mid
                                    diffimagDandretr E
                                    diffimagVandretr L
                                    hasaction None
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
        stoptrain.productionstring(name="如果实际距离<知识块距离且实际速度<知识块速度但未超过限制速度,则采用记忆中的制动", string="""
                                            =g>
                                            isa stoptrain_goal
                                            state doaction
                                            =retriveaction>
                                            isa Retriveaction
                                            action =a
                                            =judgestoptrain>
                                            isnotchangespeed yes
                                            isnotuplimit mid
                                            diffimagDandretr sameGorL
                                            diffimagVandretr sameGorL
                                            hasaction any
                                            ?manual>
                                            state   free
                                            ==>
                                            +manual>
                                            isa     _manual
                                            cmd     'press_key'
                                            key     =a
                                            ~g>
                                            ~retrieval>
                                        """)
        stoptrain.productionstring(name="比限制速度小太多，则需要释放制动", string= """
                                            =g>
                                            isa stoptrain_goal
                                            state doaction

                                            =judgestoptrain>
                                            isa Judgestoptrain
                                            isnotchangespeed yes
                                            isnotuplimit low
                                            diffimagVandretr None
                                            diffimagDandretr None
                                            hasaction None
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
        stoptrain.productionstring(name="实际速度超过限制速度，档位不可释放制动(知识块有制动)", string="""
                                            =g>
                                            isa stoptrain_goal
                                            state doaction
                                            =retriveaction>
                                            isa Retriveaction
                                            action =a
                                            =judgestoptrain>
                                            isa Judgestoptrain
                                            isnotchangespeed yes
                                            isnotuplimit up
                                            diffimagVandretr None
                                            diffimagDandretr None
                                            hasaction yes
                                            ?manual>
                                            state   free
                                            ==>
                                            +manual>
                                            isa     _manual
                                            cmd     'press_key'
                                            key     =a
                                            ~g>
                                            ~retrieval>
                                        """)
        stoptrain.productionstring(name="实际速度超过限制速度，"
                                        "档位不可释放制动(知识块无制动)",string="""
                                                    =g>
                                                    isa stoptrain_goal
                                                    state doaction
                                                    =judgestoptrain>
                                                    isa Judgestoptrain
                                                    isnotchangespeed yes
                                                    isnotuplimit up
                                                    diffimagVandretr None
                                                    diffimagDandretr None
                                                    hasaction None
                                                    ?manual>
                                                    state   free
                                                    ==>
                                                    +manual>
                                                    isa     _manual
                                                    cmd     'press_key'
                                                    key     5
                                                    ~g>
                                                    ~retrieval>
                                                """)

        stoptrain.productionstring(name="站停阶段执行0级制动，距离偏大", string="""
                                                            =g>
                                                            isa stoptrain_goal
                                                            state doaction
                                                            =judgestoptrain>
                                                            isa Judgestoptrain
                                                            isnotchangespeed disGE
                                                            isnotuplimit None
                                                            diffimagVandretr None
                                                            diffimagDandretr None
                                                            hasaction None

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
        stoptrain.productionstring(name="站停阶段执行4级制动", string="""
                                                            =g>
                                                            isa stoptrain_goal
                                                            state doaction
                                                            =judgestoptrain>
                                                            isa Judgestoptrain
                                                            isnotchangespeed stop4
                                                            isnotuplimit None
                                                            diffimagVandretr None
                                                            diffimagDandretr None
                                                            hasaction yes
                                                            ?manual>
                                                            state   free
                                                            ==>
                                                            +manual>
                                                            isa     _manual
                                                            cmd     'press_key'
                                                            key     7
                                                            ~g>
                                                            ~retrieval>
                                                        """)
        stoptrain.productionstring(name="站停阶段执行1级制动（撂闸）", string="""
                                                            =g>
                                                            isa stoptrain_goal
                                                            state doaction
                                                            =judgestoptrain>
                                                            isa Judgestoptrain
                                                            isnotchangespeed stop1
                                                            isnotuplimit up
                                                            diffimagVandretr None
                                                            diffimagDandretr None
                                                            hasaction yes
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
        stoptrain.productionstring(name="距离小于0，直接停车）", string="""
                                                                    =g>
                                                                    isa stoptrain_goal
                                                                    state doaction
                                                                    =judgestoptrain>
                                                                    isa Judgestoptrain
                                                                    isnotchangespeed stoptrain
                                                                    isnotuplimit None
                                                                    diffimagVandretr None
                                                                    diffimagDandretr None
                                                                    hasaction yes
                                                                    ?manual>
                                                                    state   free
                                                                    ==>
                                                                    +manual>
                                                                    isa     _manual
                                                                    cmd     'press_key'
                                                                    key     5
                                                                    ~g>
                                                                    ~retrieval>
                                                                """)
        stoptrain.productionstring(name="回忆失败", string="""
            =g>
            isa stoptrain_goal
            state startretrive
            ?retrieval>
            state error
            ==>
            ~g>
            ~retrieval>
        """)

        stoptrain_sim = stoptrain.simulation()
        # run the simulation
        while True:
            # print ("----------------------------------------------------------")
            try:
                stoptrain_sim.step()
            except EmptySchedule:
                break

            # 判断当前距离是否>0

            if stoptrain.goals['imaginal'] and float(stoptrain.goals['imaginal'].copy().pop()[1][1].__repr__()) > 0:
                imaginalcopy = stoptrain.goals['imaginal'].copy().pop()

                if stoptrain.retrieval:
                    # 如果回忆成功，观察回忆的知识块的内容与实际速度的出入点，进行调整档位
                    retrievalcopy = stoptrain.retrieval.copy().pop()
                    diffFordisshijiAndchunk = float(imaginalcopy[1][1].__repr__()) - float(
                        retrievalcopy[1][1].__repr__())
                    diffForVshijiAndchunk = float(imaginalcopy[2][1].__repr__()) - float(retrievalcopy[2][1].__repr__())
                    # print("实际速度与实际距离和知识块速度的差值：", diffForVshijiAndchunk, diffFordisshijiAndchunk)
                    action = int(float(retrievalcopy[0][1].__repr__()))
                    if float(imaginalcopy[2][1].__repr__()) > stopSpeed:
                        # 调速阶段
                        if float(imaginalcopy[2][1].__repr__()) <= float(
                                imaginalcopy[3][1].__repr__()) and float(
                            imaginalcopy[2][1].__repr__()) > float(imaginalcopy[3][1].__repr__()) - diffv:

                            if diffFordisshijiAndchunk > 0 and diffForVshijiAndchunk <= 0:
                                # 如果实际距离>知识块距离(未超过限速),则释放制动
                                stoptrain.goals["judgestoptrain"].add(
                                    actr.chunkstring(string=""" isa Judgestoptrain
                                                                isnotchangespeed yes
                                                                isnotuplimit mid
                                                                diffimagDandretr G
                                                                diffimagVandretr any
                                                                hasaction None
                                                                """))
                            elif diffFordisshijiAndchunk < 0 and diffForVshijiAndchunk >= 0:
                                # 如果实际距离<知识块距离,实际速度>=知识块速度且,则采取制动
                                if action <= 0:
                                    # action = 1
                                    stoptrain.goals["judgestoptrain"].add(
                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                isnotchangespeed yes
                                                                isnotuplimit mid
                                                                diffimagDandretr L
                                                                diffimagVandretr GE
                                                                hasaction None
                                                                """))
                                else:
                                    stoptrain.goals["judgestoptrain"].add(
                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                isnotchangespeed yes
                                                                isnotuplimit mid
                                                                diffimagDandretr L
                                                                diffimagVandretr GE
                                                                hasaction yes
                                                                """))

                                # print("如果记忆的档位采取制动，就采取相应的制动")
                            elif diffFordisshijiAndchunk == 0 and diffForVshijiAndchunk > 0:
                                # 如果实际距离==知识块距离,实际速度>知识块速度,则采取制动
                                if action <= 0:
                                    stoptrain.goals["judgestoptrain"].add(
                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                    isnotchangespeed yes
                                                                    isnotuplimit mid
                                                                    diffimagDandretr E
                                                                    diffimagVandretr G
                                                                    hasaction None
                                                                    """))
                                    # action = 1
                                else:
                                    stoptrain.goals["judgestoptrain"].add(
                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                isnotchangespeed yes
                                                                isnotuplimit mid
                                                                diffimagDandretr E
                                                                diffimagVandretr G
                                                                hasaction yes
                                                                """))
                                # print("距离相等，实际速度大，采取制动")
                            elif diffFordisshijiAndchunk == 0 and diffForVshijiAndchunk == 0:
                                # 如果实际距离==知识块距离且实际速度==知识块速度,则保持原档位
                                stoptrain.goals["judgestoptrain"].add(
                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                isnotchangespeed yes
                                                                isnotuplimit mid
                                                                diffimagDandretr E
                                                                diffimagVandretr E
                                                                hasaction None
                                                                """))
                            elif diffFordisshijiAndchunk == 0 and diffForVshijiAndchunk < 0:
                                # 如果实际距离==知识块距离且实际速度<知识块速度,则释放制动
                                stoptrain.goals["judgestoptrain"].add(
                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                isnotchangespeed yes
                                                                isnotuplimit mid
                                                                diffimagDandretr E
                                                                diffimagVandretr L
                                                                hasaction None
                                                                """))
                            else:
                                # 实际速度未超过限制速度，档位不可采取制动,释放制动
                                stoptrain.goals["judgestoptrain"].add(
                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                isnotchangespeed yes
                                                                isnotuplimit mid
                                                                diffimagDandretr sameGorL
                                                                diffimagVandretr sameGorL
                                                                hasaction any
                                                                """))

                        elif float(imaginalcopy[2][1].__repr__()) <= float(imaginalcopy[3][1].__repr__()) - diffv:
                            # print("比限制速度小太多，则需要释放制动")
                            # action = 0
                            stoptrain.goals["judgestoptrain"].add(
                                actr.chunkstring(string="""isa Judgestoptrain
                                                            isnotchangespeed yes
                                                            isnotuplimit low
                                                            diffimagVandretr None
                                                            diffimagDandretr None
                                                            hasaction None
                                                            """))
                        else:
                            # print("实际速度超过限制速度，档位不可释放制动")
                            # if action == 0:
                            #     # action = 1

                            stoptrain.goals["judgestoptrain"].add(
                                actr.chunkstring(string="""isa Judgestoptrain
                                                            isnotchangespeed yes
                                                            isnotuplimit up
                                                            diffimagVandretr None
                                                            diffimagDandretr None
                                                            hasaction None
                                                            """))

                    # else:
                    #     stoptrain.goals["judgestoptrain"].add(
                    #         actr.chunkstring(string="""isa Judgestoptrain
                    #                                 isnotchangespeed yes
                    #                                 isnotuplimit up
                    #                                 diffimagVandretr None
                    #                                 diffimagDandretr None
                    #                                 hasaction yes
                    #                                 """))

                    else:
                        # 站停阶段，速度36的时候以及制动距离为500m
                        if float(imaginalcopy[1][1].__repr__()) > 169.2:
                            # 超过150m速度大于
                            # 距离偏大，释放制动
                            # 欠标和超标两种情况
                            # action = 0
                            stoptrain.goals["judgestoptrain"].add(
                                actr.chunkstring(string="""isa Judgestoptrain
                                                            isnotchangespeed disGE
                                                            isnotuplimit None
                                                            diffimagVandretr None
                                                            diffimagDandretr None
                                                            hasaction None
                                                            """))

                        else:
                            if float(imaginalcopy[2][1].__repr__()) >= 15:
                                # action = 1，撂闸1级制动
                                stoptrain.goals["judgestoptrain"].add(
                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                isnotchangespeed stop1
                                                                isnotuplimit up
                                                                diffimagVandretr None
                                                                diffimagDandretr None
                                                                hasaction yes
                                                                """))
                            else:
                                if float(imaginalcopy[1][1].__repr__()) >= 98.5:
                                    stoptrain.goals["judgestoptrain"].add(
                                        actr.chunkstring(string="""isa Judgestoptrain
                                                            isnotchangespeed disGE
                                                            isnotuplimit None
                                                            diffimagVandretr None
                                                            diffimagDandretr None
                                                            hasaction None
                                                            """))

                                else:
                                    if float(imaginalcopy[2][1].__repr__()) >= 12:
                                        # action = 1，撂闸1级制动
                                        stoptrain.goals["judgestoptrain"].add(
                                            actr.chunkstring(string="""isa Judgestoptrain
                                                                        isnotchangespeed stop1
                                                                        isnotuplimit up
                                                                        diffimagVandretr None
                                                                        diffimagDandretr None
                                                                        hasaction yes
                                                                        """))
                                    else:
                                        if float(imaginalcopy[1][1].__repr__()) >= 64.5:
                                            stoptrain.goals["judgestoptrain"].add(
                                                actr.chunkstring(string="""isa Judgestoptrain
                                                                    isnotchangespeed disGE
                                                                    isnotuplimit None
                                                                    diffimagVandretr None
                                                                    diffimagDandretr None
                                                                    hasaction None
                                                                    """))

                                        else:
                                            if float(imaginalcopy[2][1].__repr__()) >= 10:
                                                # action = 1，撂闸1级制动
                                                stoptrain.goals["judgestoptrain"].add(
                                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                                isnotchangespeed stop1
                                                                                isnotuplimit up
                                                                                diffimagVandretr None
                                                                                diffimagDandretr None
                                                                                hasaction yes
                                                                                """))
                                            else:
                                                if float(imaginalcopy[1][1].__repr__()) >= 47:
                                                    stoptrain.goals["judgestoptrain"].add(
                                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                            isnotchangespeed disGE
                                                                            isnotuplimit None
                                                                            diffimagVandretr None
                                                                            diffimagDandretr None
                                                                            hasaction None
                                                                            """))

                                                else:
                                                    if float(imaginalcopy[2][1].__repr__()) >= 9:
                                                        # action = 1，撂闸1级制动
                                                        stoptrain.goals["judgestoptrain"].add(
                                                            actr.chunkstring(string="""isa Judgestoptrain
                                                                                        isnotchangespeed stop1
                                                                                        isnotuplimit up
                                                                                        diffimagVandretr None
                                                                                        diffimagDandretr None
                                                                                        hasaction yes
                                                                                        """))
                                                    else:
                                                        if float(imaginalcopy[1][1].__repr__()) >= 36.9:
                                                            stoptrain.goals["judgestoptrain"].add(
                                                                actr.chunkstring(string="""isa Judgestoptrain
                                                                                    isnotchangespeed disGE
                                                                                    isnotuplimit None
                                                                                    diffimagVandretr None
                                                                                    diffimagDandretr None
                                                                                    hasaction None
                                                                                    """))

                                                        else:

                                                            if float(imaginalcopy[2][1].__repr__()) >= 8:
                                                                # action = 1，撂闸1级制动
                                                                stoptrain.goals["judgestoptrain"].add(
                                                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                                                isnotchangespeed stop1
                                                                                                isnotuplimit up
                                                                                                diffimagVandretr None
                                                                                                diffimagDandretr None
                                                                                                hasaction yes
                                                                                                """))
                                                            else:
                                                                if float(imaginalcopy[1][1].__repr__()) >= 29.2:
                                                                    stoptrain.goals["judgestoptrain"].add(
                                                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                                            isnotchangespeed disGE
                                                                                            isnotuplimit None
                                                                                            diffimagVandretr None
                                                                                            diffimagDandretr None
                                                                                            hasaction None
                                                                                            """))

                                                                else:

                                                                    if float(imaginalcopy[2][1].__repr__()) >= 7:
                                                                        # action = 1，撂闸1级制动
                                                                        stoptrain.goals["judgestoptrain"].add(
                                                                            actr.chunkstring(string="""isa Judgestoptrain
                                                                                                        isnotchangespeed stop1
                                                                                                        isnotuplimit up
                                                                                                        diffimagVandretr None
                                                                                                        diffimagDandretr None
                                                                                                        hasaction yes
                                                                                                        """))
                                                                    else:
                                                                        if float(imaginalcopy[1][1].__repr__()) >= 22.9:
                                                                            stoptrain.goals["judgestoptrain"].add(
                                                                                actr.chunkstring(string="""isa Judgestoptrain
                                                                                                    isnotchangespeed disGE
                                                                                                    isnotuplimit None
                                                                                                    diffimagVandretr None
                                                                                                    diffimagDandretr None
                                                                                                    hasaction None
                                                                                                    """))

                                                                        else:
                                                                            if float(imaginalcopy[2][1].__repr__()) >= 6:
                                                                                # action = 1，撂闸1级制动
                                                                                stoptrain.goals["judgestoptrain"].add(
                                                                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                isnotchangespeed stop1
                                                                                                                isnotuplimit up
                                                                                                                diffimagVandretr None
                                                                                                                diffimagDandretr None
                                                                                                                hasaction yes
                                                                                                                """))
                                                                            else:
                                                                                if float(imaginalcopy[1][1].__repr__()) >= 16.7:
                                                                                    stoptrain.goals["judgestoptrain"].add(
                                                                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                                                            isnotchangespeed disGE
                                                                                                            isnotuplimit None
                                                                                                            diffimagVandretr None
                                                                                                            diffimagDandretr None
                                                                                                            hasaction None
                                                                                                            """))

                                                                                else:
                                                                                    if float(imaginalcopy[2][1].__repr__()) >= 5:
                                                                                        # action = 1，撂闸1级制动
                                                                                        stoptrain.goals["judgestoptrain"].add(
                                                                                            actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                        isnotchangespeed stop1
                                                                                                                        isnotuplimit up
                                                                                                                        diffimagVandretr None
                                                                                                                        diffimagDandretr None
                                                                                                                        hasaction yes
                                                                                                                        """))
                                                                                    else:
                                                                                        if float(imaginalcopy[1][1].__repr__()) >= 11.6:
                                                                                            stoptrain.goals["judgestoptrain"].add(
                                                                                                actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                    isnotchangespeed disGE
                                                                                                                    isnotuplimit None
                                                                                                                    diffimagVandretr None
                                                                                                                    diffimagDandretr None
                                                                                                                    hasaction None
                                                                                                                    """))

                                                                                        else:


                                                                                            if float(imaginalcopy[2][1].__repr__()) >= 3:
                                                                                                # action = 1，撂闸1级制动
                                                                                                stoptrain.goals["judgestoptrain"].add(
                                                                                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                                isnotchangespeed stop1
                                                                                                                                isnotuplimit up
                                                                                                                                diffimagVandretr None
                                                                                                                                diffimagDandretr None
                                                                                                                                hasaction yes
                                                                                                                                """))
                                                                                            else:
                                                                                                if float(imaginalcopy[1][1].__repr__()) >= 4.2:
                                                                                                    stoptrain.goals["judgestoptrain"].add(
                                                                                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                            isnotchangespeed disGE
                                                                                                                            isnotuplimit None
                                                                                                                            diffimagVandretr None
                                                                                                                            diffimagDandretr None
                                                                                                                            hasaction None
                                                                                                                            """))

                                                                                                else:
                                                                                                    if float(imaginalcopy[2][1].__repr__()) >= 2:
                                                                                                        # action = 1，撂闸1级制动
                                                                                                        stoptrain.goals["judgestoptrain"].add(
                                                                                                            actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                                        isnotchangespeed stop1
                                                                                                                                        isnotuplimit up
                                                                                                                                        diffimagVandretr None
                                                                                                                                        diffimagDandretr None
                                                                                                                                        hasaction yes
                                                                                                                                        """))
                                                                                                    else:
                                                                                                        if float(imaginalcopy[1][1].__repr__()) >= 1.9:
                                                                                                            stoptrain.goals["judgestoptrain"].add(
                                                                                                                actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                                    isnotchangespeed disGE
                                                                                                                                    isnotuplimit None
                                                                                                                                    diffimagVandretr None
                                                                                                                                    diffimagDandretr None
                                                                                                                                    hasaction None
                                                                                                                                    """))

                                                                                                        else:



                                                                                                            if float(imaginalcopy[2][1].__repr__()) >= 0.9:
                                                                                                                # action = 1，撂闸1级制动
                                                                                                                stoptrain.goals["judgestoptrain"].add(
                                                                                                                    actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                                                isnotchangespeed stop1
                                                                                                                                                isnotuplimit up
                                                                                                                                                diffimagVandretr None
                                                                                                                                                diffimagDandretr None
                                                                                                                                                hasaction yes
                                                                                                                                                """))
                                                                                                            else:
                                                                                                                if float(imaginalcopy[1][1].__repr__()) >= 0.4:
                                                                                                                    stoptrain.goals["judgestoptrain"].add(
                                                                                                                        actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                                                    isnotchangespeed stop4
                                                                                                                                                    isnotuplimit up
                                                                                                                                                    diffimagVandretr None
                                                                                                                                                    diffimagDandretr None
                                                                                                                                                    hasaction yes
                                                                                                                                                    """))
                                                                                                                else:
                                                                                                                    if float(imaginalcopy[2][
                                                                                                                                 1].__repr__()) >= 0.5:
                                                                                                                        # action = 1，撂闸1级制动
                                                                                                                        stoptrain.goals[
                                                                                                                            "judgestoptrain"].add(
                                                                                                                            actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                                                        isnotchangespeed stop1
                                                                                                                                                        isnotuplimit up
                                                                                                                                                        diffimagVandretr None
                                                                                                                                                        diffimagDandretr None
                                                                                                                                                        hasaction yes
                                                                                                                                                        """))
                                                                                                                    else:
                                                                                                                        if float(imaginalcopy[1][
                                                                                                                                     1].__repr__()) >= 0.2:
                                                                                                                            stoptrain.goals[
                                                                                                                                "judgestoptrain"].add(
                                                                                                                                actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                                                            isnotchangespeed stop4
                                                                                                                                                            isnotuplimit up
                                                                                                                                                            diffimagVandretr None
                                                                                                                                                            diffimagDandretr None
                                                                                                                                                            hasaction yes
                                                                                                                                                            """))
                                                                                                                        else:




                                                                                                                            stoptrain.goals["judgestoptrain"].add(
                                                                                                                                actr.chunkstring(string="""isa Judgestoptrain
                                                                                                                                                            isnotchangespeed stop4
                                                                                                                                                            isnotuplimit up
                                                                                                                                                            diffimagVandretr None
                                                                                                                                                            diffimagDandretr None
                                                                                                                                                            hasaction yes
                                                                                                                                                            """))

            else:
                stoptrain.goals["judgestoptrain"].add(
                    actr.chunkstring(string="""isa Judgestoptrain
                                                isnotchangespeed stoptrain
                                                isnotuplimit None
                                                diffimagVandretr None
                                                diffimagDandretr None
                                                hasaction yes
                                                """))

            if stoptrain_sim.current_event[2][:-1] == 'KEY PRESSED: ':
                print("当前按键档位为：", stoptrain_sim.current_event[2][-1])
                action = int(stoptrain_sim.current_event[2][-1])

        alltime=stoptrain_sim.show_time()
        print("actr输出的action:", action)
        return action,alltime


if __name__ == "__main__":
    currentSforplt, currentVforplt, nexVforplt, actionforplt,accValueForplt,timeForeach = [], [], [], [], [],[]
    currentV0, currentS0 = 278, 9155.7
    sys.stdout = open(r"..\pyactrforstoptrain1\result\actrresult_{0:}_{1:}.txt".format(currentV0,currentS0), "w")
    a1 = actrmodel()
    # ----------------------------加速度------------------------------------------------
    # a11, a2, a3, a4, a5, a6, a7,x10 = [], [], [], [], [], [], [],[]
    # for i in range(350):
    #     acc1 = a1.updatecurrentVandS(i, currentS=10, action=1, double_dT=1)
    #     a11.append(acc1[2])
    #     acc2 = a1.updatecurrentVandS(i, currentS=10, action=2, double_dT=1)
    #     a2.append(acc2[2])
    #     acc3 = a1.updatecurrentVandS(i, currentS=10, action=3, double_dT=1)
    #     a3.append(acc3[2])
    #     acc4 = a1.updatecurrentVandS(i, currentS=10, action=4, double_dT=1)
    #     a4.append(acc4[2])
    #     acc5 = a1.updatecurrentVandS(i, currentS=10, action=5, double_dT=1)
    #     a5.append(acc5[2])
    #     acc6 = a1.updatecurrentVandS(i, currentS=10, action=6, double_dT=1)
    #     a6.append(acc6[2])
    #     acc7 = a1.updatecurrentVandS(i, currentS=10, action=7, double_dT=1)
    #     a7.append(acc7[2])
    #     x10.append(i)
    # plt.figure(1)
    # # plt.axis([max(x10), -200, 0, max(nexVforplt) + 1])
    # plt.plot(x10, a11, linestyle="-", linewidth=1,
    #          label='a1')
    # plt.plot(x10, a2, linestyle="--", linewidth=1,
    #          label='a2')
    # plt.plot(x10, a3, linestyle="-.", linewidth=1,
    #          label='a3')
    # plt.plot(x10, a4, linestyle="dashed", linewidth=1,
    #          label='a4')
    # plt.plot(x10, a5, linestyle="dashdot", linewidth=1,
    #          label='a5')
    # plt.plot(x10, a6, linestyle="dotted", linewidth=1,
    #          label='a6')
    # plt.plot(x10, a7, linestyle='', linewidth=1,
    #          label='a7')
    # plt.legend()
    # plt.savefig(r"..\pyactrforstoptrain\acc.png")
    # plt.show()
    # ----------------------------加速度------------------------------------------------
    # 270, 300, 9155.7, 3正确初始条件


    currentV, nexV, currentS, action = currentV0, 300, currentS0, 3
    pidactionforplt, pidnextv, pidcurrentVforplt, pidcurrentsforplt = [], [], [], []
    pidcount = 0
    runtime=0
    accValue=0

    # 保存前一个速度
    preaction=[action]
    isActionChange=[action]
    timechange=0
    while currentV > 0:
        print("---------------------------------------------------")
        print("更新后的速度、限速以及距离：", round(currentV, 1), round(nexV, 1), round(currentS, 1))
        action,alltime = a1.actrsim(currentv=round(currentV, 1), nextv=round(nexV, 1), currentd=round(currentS, 1))
        # print("当前挡位和上次制动的挡位：", action, isActionChange[-1],isActionChange)
        if action != isActionChange[-1]:
            timechange += 1

        if isActionChange[-1]-action>=2:
            action=max(0,isActionChange[-1]-1)
            print("调整了速度")
        if action-isActionChange[-1]>=2:
            action=max(0,isActionChange[-1]+1)

        isActionChange.append(action)
        print("调整后的最终档位:", action)
        print("调整次数:", timechange)

        """
        保存前一个时刻的制动级位，带入到当前程序中，判断速度距离经验值相差有多远。
        ①如果前一时刻的挡位带到当前速度中与优化速度依旧再速度误差范围中，则优先选用前一时刻的制动级外
        """
        # print("sdfsdfsdfsd", float(currentV * 1000 / 3600), float(currentS), action)
        updatecurVandS = a1.updatecurrentVandS(float(currentV * 1000 / 3600), float(currentS), action,double_dT=alltime)

        updatenexVandS = a1.updatenextVandS(float(currentV), float(currentS))

        nexV = updatenexVandS[0]

        # ++++++++++++++++++++++++++增加了对先前挡位的考虑++++++++++++++++++++++++++
        # if abs(action-actionforplt[-1])>
        # ++++++++++++++++++++++++++增加了对先前挡位的考虑++++++++++++++++++++++++++
        # print("最终调整后挡位",action)

        currentV = updatecurVandS[0] * 3600 / 1000
        currentS = updatecurVandS[1]
        accValue= updatecurVandS[2]
        runtime +=alltime

        # 绘图作用
        timeForeach.append(alltime)
        accValueForplt.append(accValue)
        actionforplt.append(action)
        currentSforplt.append(currentS)
        currentVforplt.append(currentV)
        nexVforplt.append(nexV)

    # 计算舒适度
    comfort=0
    # 惰行制动时间
    timezerolevel=0
    for i in range(len(accValueForplt)):
        comfort += accValueForplt[i]/timeForeach[i]
        if accValueForplt[i]==0:
            timezerolevel +=timeForeach[i]

    print("停车速度和距离：", currentVforplt[-1], currentSforplt[-1])

    print("停车调整次数：", timechange)
    print("停车制动时间：", runtime)
    print("act-r模型控制非舒适度：",comfort)
    print("act-r模型控制惰行制动时间：",timezerolevel)
    for i in range(len(currentVforplt)):
        with open(r"..\pyactrforstoptrain1\\chunk.csv", "a+") as f:
            f.write("%d; %e; %e; %e \n" % (actionforplt[i], currentVforplt[i], nexVforplt[i], currentSforplt[i]))

    plt.figure(1)
    plt.subplot(211)
    plt.axis([max(currentSforplt), -200, 0, max(nexVforplt) + 1])

    plt.plot(currentSforplt, currentVforplt, linestyle="-", linewidth=1,
             label='trainspeed')
    plt.plot(currentSforplt, nexVforplt, linestyle="-", linewidth=1,
             label='speed limit')
    plt.legend()

    # plt.subplot(212)
    # plt.axis([max(currentSforplt), -200, 0, max(accValueForplt)])
    # plt.plot(currentSforplt, accValueForplt, linestyle="-", linewidth=1,
    #          label='acc')
    # plt.legend()

    plt.subplot(212)
    plt.axis([max(currentSforplt), -200, 0, max(actionforplt)])
    plt.plot(currentSforplt, actionforplt, linestyle="-", linewidth=1,
             label='action')
    plt.legend()
    plt.savefig(r"../pyactrforstoptrain1/result/similfprchunk_{0:}_{1:}.png".format(currentV0, currentS0))
    plt.show()
    print("仿真结束")
    # break

    A = np.array(currentSforplt)
    B = np.array(nexVforplt)
    C = np.array(currentVforplt)
    D = np.array(actionforplt)
    E = np.array(accValueForplt)
    data = pd.DataFrame(A)
    data_1 = pd.DataFrame(B)
    data_2 = pd.DataFrame(C)
    data_3 = pd.DataFrame(D)
    data_4 = pd.DataFrame(E)
    writer = pd.ExcelWriter('../pyactrforstoptrain1/result/初速度为{0:}_初始距离为{1:}_result_actr.xlsx'.format(currentV0,currentS0),mode="w")  # 写入Excel文件
    data.to_excel(writer, 'ACT-R', float_format='%.5f', header=False, index=False, startrow=0, startcol=0, )
    data_1.to_excel(writer, 'ACT-R', float_format='%.5f', header=False, index=False, startrow=0, startcol=1, )
    data_2.to_excel(writer, 'ACT-R', float_format='%.5f', header=False, index=False, startrow=0, startcol=2, )
    data_3.to_excel(writer, 'ACT-R', float_format='%.5f', header=False, index=False, startrow=0, startcol=3, )
    data_4.to_excel(writer, 'ACT-R', float_format='%.5f', header=False, index=False, startrow=0, startcol=4, )
    writer.save()
    writer.close()
    print("----------------------------------程序运行结果已经保存到/result/result_actr.xlsx中----------------------------------")

