# /usr/bin/env python
# -*- coding: UTF-8 -*-
# 本文列车动力学模型中每个级位对应的加速度
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def sdfs(wqe=232, aha=1212):
    pass
x10 = [x for x in range(350)]

a1, a2, a3, a4, a5, a6, a7, nextvforplt = [], [], [], [], [], [], [], []
for i in range(0, 10):
    acc1 = 0.07875 + 0.003375 * i
    acc2 = 0.1575 + 0.00675 * i
    acc3 = 0.23625 + 0.010125 * i
    acc4 = 0.315 + 0.0135 * i
    acc5 = 0.371 + 0.02023328 * i

    if i < 5:
        acc6 = 0.515
        acc7 = 0.5635
    else:
        acc6 = 0.435 + 0.0160 * i
        acc7 = 0.483 + 0.0161 * i
    a1.append(acc1)
    a2.append(acc2)
    a3.append(acc3)
    a4.append(acc4)
    a5.append(acc5)
    a6.append(acc6)
    a7.append(acc7)
for i in range(10, 160):
    acc1 = 0.1125
    acc2 = 0.225
    acc3 = 0.3375
    acc4 = 0.45
    acc5 = 0.5733328

    if i <= 20:
        acc6 = 0.435 + 0.0160 * i
        acc7 = 0.483 + 0.0161 * i
    else:
        acc6 = 0.755
        acc7 = 0.805
    a1.append(acc1)
    a2.append(acc2)
    a3.append(acc3)
    a4.append(acc4)
    a5.append(acc5)
    a6.append(acc6)
    a7.append(acc7)
for i in range(160, 240):
    acc1 = 0.1975 - 0.00053125 * i  # 240=0.07
    acc2 = 0.395 - 0.0010625 * i  # 240=0.14
    acc3 = 0.5925 - 0.00159375 * i  # 240=0.21
    acc4 = 0.79 - 0.002125 * i  # 240=0.28
    acc5 = 1.02 - 0.00279167 * i  # 240=0.35
    acc6 = 1.378 - 0.00389375 * i  # 240=0.4435
    acc7 = 1.47 - 0.00415625 * i  # 240=0.4725
    a1.append(acc1)
    a2.append(acc2)
    a3.append(acc3)
    a4.append(acc4)
    a5.append(acc5)
    a6.append(acc6)
    a7.append(acc7)
for i in range(240, 350):
    acc1 = 0.117142857 - 0.000196429 * i
    acc2 = 0.234285714 - 0.0003928571416 * i
    acc3 = 0.351428571 - 0.0005892857125 * i
    acc4 = 0.468571429 - 0.000785714 * i
    acc5 = 0.585714285 - 0.0009821428541 * i
    acc6 = 0.774857141992 - 0.0013806547583 * i
    acc7 = 0.8325 - 0.0015 * i

    a1.append(acc1)
    a2.append(acc2)
    a3.append(acc3)
    a4.append(acc4)
    a5.append(acc5)
    a6.append(acc6)
    a7.append(acc7)

plt.figure(1)
# plt.axis([max(x10), -200, 0, max(nexVforplt) + 1])
plt.plot(x10, a1, linestyle="-", linewidth=1,
         label='a1挡位')
plt.plot(x10, a2, linestyle="-", linewidth=1,
         label='a2挡位')
plt.plot(x10, a3, linestyle="-", linewidth=1,
         label='a3挡位')
plt.plot(x10, a4, linestyle="-", linewidth=1,
         label='a4挡位')
plt.plot(x10, a5, linestyle="-", linewidth=1,
         label='a5挡位')
plt.plot(x10, a6, linestyle="-", linewidth=1,
         label='a6挡位')
plt.plot(x10, a7, linestyle="-", linewidth=1,
         label='a7挡位')

plt.xlabel(u'速度（单位：km/h）')
plt.ylabel(u'加速度（单位：m/$\mathregular{s^2}$）')
plt.legend()
plt.savefig("../pyactrforstoptrain1/result/accTospeed.png")
plt.show()

