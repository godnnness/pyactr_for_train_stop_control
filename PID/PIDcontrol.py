# /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Author  : Yulong Sun
# @FileName: ceshi.py
# @Software: PyCharm
# @Blog    ：https://github.com/godnnness/trainforactr


#this code refer to CSDN and do some minor change.

import time

class stopTrainInPID:

    def __init__(self, P, I, D,windup_guard):#初始化
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.windup_guard=windup_guard
        self.clear()


    def clear(self):
        self.SetLevel = 0.0#期望速度
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.windup_guard=0.0
        self.output = 0.0

    def update(self, feedback_value):
        error = self.SetLevel - feedback_value
        # self.adderror.append(error)

        #比例环
        self.PTerm = self.Kp * error
        #积分环
        self.ITerm += error
        if (self.ITerm < -self.windup_guard):
            self.ITerm = -self.windup_guard
        elif (self.ITerm > self.windup_guard):
            self.ITerm = self.windup_guard
        #微分环
        delta_error = error-self.last_error
        self.DTerm = delta_error
        self.last_error = error
        # print("error（SetLevel - current_level）:", error)
        # print("delta_error",delta_error)
        # print("adderror,min,max",self.adderror,min(self.adderror),max(self.adderror))
        #输出
        print("error:",error)
        print("PTerm,ITerm,DTerm:",self.PTerm,self.ITerm,self.DTerm)
        self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
