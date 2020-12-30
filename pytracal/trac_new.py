# /usr/bin/env python
# -*- coding: UTF-8 -*-
from ctypes import *
import matplotlib.pyplot as plt
import random

"""
void run(double m_fCurVelocity, int drawhand, int breakhand, double dT, double result[])
    double m_fCurVelocity ---- 初始速度（米/秒）
    int drawhand ---- 牵引级位（0~10级，制动级位为0时激活）
    int breakhand ---- 制动级位（0~7级，8为紧急制动）
    double dT ---- 时长（秒）
    result[0] ---- 当前速度（米/秒）;
    result[1] ---- dT时长的走行距离（米）;
"""


def trac_new_speed(initspeed, breakhead, double_dT):
    tracdll = CDLL(r"C:\Users\syl\Desktop\pyactrforstoptrain\pytracal\tracal.dll")
    result = (c_double * 2)()
    tracdll.run.argtypes = [c_double, c_int, c_int, c_double]
    tracdll.run(initspeed, 0, breakhead, double_dT, result)
    # print "速度：",result[0]
    # print"{}s内走过的距离：".format(double_dT),result[1]
    return result

