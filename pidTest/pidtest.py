import time
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from pidTest.pid import PID,updatecurrentVandS

def test_pid(P=0.2, I=0.0, D=0.0):
    pid = PID(P, I, D)

    pid.SetPoint = 0.0
    pid.setSampleTime(0.01)


    currentV, nexV, currentS, action = 270, 300, 9155.7, 3
    pidactionforplt, pidnextv, pidcurrentVforplt, pidcurrentsforplt, accforplt, timeforeach = [], [], [], [], [], []

    while currentV > 0:
        nextvpid = 0.042816923306331967 * (currentS ** 1) - 1.4556065943953415e-06 * (currentS ** 2)
        pid.update(currentV)
        speedgain = pid.output
        print(speedgain)


        if speedgain > 0:
            # 每秒减少1级制动挡位
            action = action - 1
            action = max(0, action)
        elif speedgain == 0:
            action = 0
        else:
            # 每秒增加1级制动挡位
            action = action + 1
            action = min(5, action)

        pid.SetPoint = nextvpid
        updatecurVandS = updatecurrentVandS(float(currentV * 1000 / 3600), float(currentS), action, double_dT=1,delaytime=0)

        currentV=updatecurVandS[0] * 3600 / 1000
        currentS = updatecurVandS[1]


        pidactionforplt.append(action)
        pidcurrentVforplt.append(currentV)
        pidcurrentsforplt.append(currentS)
        pidnextv.append(nextvpid)
    A = np.array([pidactionforplt, pidcurrentVforplt, pidnextv, pidcurrentsforplt]).T
    print("pid完成并退出", pidcurrentsforplt[-1], pidcurrentVforplt[-1])
    # print("pid控制次数和距离：", pidcount, pidcurrentsforplt[-1])
    # print("pid调整次数：", timeSpeedChange)

    plt.figure(1)
    plt.subplot(121)
    plt.axis([max(pidcurrentsforplt), -200, 0, max(pidnextv) + 1])
    plt.plot(pidcurrentsforplt, pidnextv, linestyle="-", linewidth=1,
             label='pidnextv')
    plt.plot(pidcurrentsforplt, pidcurrentVforplt, linestyle="-", linewidth=1,
             label='pidcurrentVforplt')

    plt.legend()
    plt.subplot(122)
    plt.plot(pidcurrentsforplt, pidactionforplt, linestyle="-", linewidth=1,
             label='pidactionforplt')
    plt.legend()
    plt.savefig("./images/similfprpid.png")
    plt.show()

if __name__ == "__main__":
    test_pid(1.2, 1.0, 0.001)
