# /usr/bin/env python
# -*- coding: UTF-8 -*-
from ctypes import *
"""
void run(double m_fCurVelocity, int drawhand, int breakhand, double dT, double result[])
    double m_fCurVelocity ---- 初始速度（米/秒）
    int drawhand ---- 牵引级位（0~10级，制动级位为0时激活）
    int breakhand ---- 制动级位（0~7级，8为紧急制动）
    double dT ---- 时长（秒）
    result[0] ---- 当前速度（米/秒）;
    result[1] ---- dT时长的走行距离（米）;
"""
# 10ms仿真周期，400km
if __name__ == "__main__":

    tracdll = CDLL("tracal64.dll")
    result = (c_double * 2)()
    tracdll.run.argtypes = [c_double, c_int, c_int, c_double]
    tracdll.run(10.0, 0, 1, 15.0, result)
    print (result[0], result[1])
