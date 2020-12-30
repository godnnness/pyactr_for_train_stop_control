# -*- coding: utf-8 -*-
import time


class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time
        self.clear()

    def clear(self):
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.int_error = 0.0
        self.windup_guard = 20.0
        self.output = 0.0

    def update(self, feedback_value):
        error = self.SetPoint - feedback_value
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error
        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error  # 比例
            self.ITerm += error * delta_time  # 积分
            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard
            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time
            self.last_time = self.current_time
            self.last_error = error
            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time

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

    global acc, currentVt
    if action==0:
        acc=0
        currentVt=currentV

    elif action==1:
        if 0<=currentV<=10:
            acc=0.07875+0.003375*currentV
            currentVt=currentV-acc*(double_dT+delaytime)
        elif 10<currentV<=160:
            acc = 0.1125
            currentVt = currentV - acc * (double_dT +delaytime)
        elif 160<currentV<=240:
            acc = (0.1975-0.00053125*currentV)
            currentVt = currentV - acc* (double_dT +delaytime)
        else:
            #240<currentV<=350
            acc = (0.117142857 - 0.000196429 * currentV)
            currentVt = currentV - acc * (double_dT +delaytime)
    elif action==2:
        if 0<=currentV<=10:
            acc=0.1575 + 0.00675*currentV
            currentVt=currentV-acc*(double_dT+delaytime)
        elif 10<currentV<=160:
            acc = 0.225
            currentVt = currentV - acc * (double_dT +delaytime)
        elif 160<currentV<=240:
            acc = 0.395 - 0.0010625*currentV
            currentVt = currentV - acc* (double_dT +delaytime)
        else:
            #240<currentV<=350
            acc = 0.234285714 - 0.0003928571416 * currentV
            currentVt = currentV - acc * (double_dT +delaytime)
    elif action==3:
        if 0<=currentV<=10:
            acc=0.23625 + 0.010125*currentV
            currentVt=currentV-acc*(double_dT+delaytime)
        elif 10<currentV<=160:
            acc = 0.3375
            currentVt = currentV - acc * (double_dT +delaytime)
        elif 160<currentV<=240:
            acc = 0.5925 - 0.00159375 *currentV
            currentVt = currentV - acc* (double_dT +delaytime)
        else:
            #240<currentV<=350
            acc = 0.351428571 - 0.0005892857125 * currentV
            currentVt = currentV - acc * (double_dT +delaytime)
    elif action==4:
        if 0<=currentV<=10:
            acc=(0.315+0.0135*currentV)
            currentVt=currentV-acc*(double_dT+delaytime)
        elif 10<currentV<=160:
            acc=0.45
            currentVt = currentV - acc * (double_dT +delaytime)
        elif 160<currentV<=240:
            acc=0.79-0.002125*currentV
            currentVt = currentV - acc* (double_dT +delaytime)
        else:
            #240<currentV<=350
            acc=0.468571429 - 0.000785714 * currentV
            currentVt = currentV - acc * (double_dT +delaytime)
    elif action==5:
        if 0<=currentV<=10:
            acc=0.371 + 0.02023328*currentV
            currentVt=currentV-acc*(double_dT+delaytime)
        elif 10<currentV<=160:
            acc=0.5733328
            currentVt = currentV - acc * (double_dT +delaytime)
        elif 160<currentV<=240:
            acc=1.02 - 0.00279167 * currentV
            currentVt = currentV - acc* (double_dT +delaytime)
        else:
            #240<currentV<=350
            acc=0.585714285 - 0.0009821428541 * currentV
            currentVt = currentV - acc * (double_dT +delaytime)
    elif action==6:
        if 0<=currentV<=5:
            acc=0.515
            currentVt=currentV-acc*(double_dT+delaytime)
        elif 5<=currentV<=20:
            acc=0.435+0.0160 * currentV
            currentVt=currentV-acc*(double_dT+delaytime)
        elif 20<currentV<=160:
            acc=0.755
            currentVt = currentV - acc * (double_dT +delaytime)
        elif 160<currentV<=240:
            acc=1.378 - 0.00389375 * currentV
            currentVt = currentV - acc* (double_dT +delaytime)
        else:
            #240<currentV<=350
            acc=0.774857141992 - 0.0013806547583 * currentV
            currentVt = currentV - acc * (double_dT +delaytime)
    elif action==7:
        if 0 <= currentV <= 5:
            acc=0.5635
            currentVt = currentV -  acc* (double_dT +delaytime)
        elif 5 < currentV <= 20:
            acc=0.483 + 0.0161 * currentV
            currentVt = currentV - acc* (double_dT +delaytime)
        elif 20 < currentV <= 160:
            acc=0.805
            currentVt = currentV - acc * (double_dT +delaytime)
        elif 160 < currentV <= 240:
            acc=1.47-0.00415625* currentV
            currentVt = currentV - acc * (double_dT +delaytime)
        else:
            # 240<currentV<=350
            acc = 0.8325-0.0015 * currentV
            currentVt = currentV - acc * (double_dT +delaytime)
    else:
        #纯空气紧急制动action == 8
        if 0 <= currentV <= 250:
            acc = 0.98
            currentVt = currentV - acc * (double_dT +delaytime)
        elif 250 < currentV <= 300:
            acc = 0.75
            currentVt = currentV - acc* (double_dT +delaytime)
        else:
            # 300 < currentV <= 350
            acc = 0.40
            currentVt = currentV - 0.40 * (double_dT +delaytime)

    if action==0:
        currentS = currentS - currentV * double_dT
    else:
        currentS = currentS + (currentVt ** 2 - currentV ** 2) / (2 * acc)


    # newresult = trac_new.trac_new_speed(currentV, int(float(action)), 10)
    # currentS = currentS - newresult[1]
    # currentV = newresult[0]
    VandS = [currentVt, currentS]
    return VandS
