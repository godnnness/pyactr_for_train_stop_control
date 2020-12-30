# /usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt
a4=5.0

print(a4//2)
kp2_5,p1k_5,p2p3_5= 375,47,320
kp2_95,p1k_95,p2p3_95= 425,64,433
hxforplt5,hyforplt5=[],[]
hxforplt95,hyforplt95=[],[]
# 百分之5
A1=[i for i in range(15,26)]
A2=[i for i in range(85,101)]
# print(A1,A2,math.cos(180*(math.pi/180)))
for a1 in A1:
    for a2 in A2:
        # hx和hy坐标
        hx=(kp2_5*math.cos((180-a1-a2)*(math.pi/180))+p2p3_5*math.cos(a4*(math.pi/180))-p1k_5*math.cos(a1*(math.pi/180)))
        hy=kp2_5*math.sin((180-a1-a2)*(math.pi/180))+p1k_5*math.sin(a1*(math.pi/180))-p2p3_5*math.sin(a4*(math.pi/180))
        hxforplt5.append(hx)
        hyforplt5.append(hy)
# 百分之95
for a1 in A1:
    for a2 in A2:
        # hx和hy坐标
        hx=(kp2_95*math.cos((180-a1-a2)*(math.pi/180))+p2p3_95*math.cos(a4*(math.pi/180))-p1k_95*math.cos(a1*(math.pi/180)))
        hy=kp2_95*math.sin((180-a1-a2)*(math.pi/180))+p1k_95*math.sin(a1*(math.pi/180))-p2p3_95*math.sin(a4*(math.pi/180))
        hxforplt95.append(hx)
        hyforplt95.append(hy)
# print(hxforplt5,hyforplt5)
# print(hxforplt95,hyforplt95)
print("x5,x95",min(hxforplt5),max(hxforplt5),min(hxforplt95),max(hxforplt95))
print("y5,y95",min(hyforplt5),max(hyforplt5),min(hyforplt95),max(hyforplt95))
print(max(hyforplt5)-min(hyforplt5),max(hxforplt5)-min(hxforplt5))
xmin= min(min(hxforplt5),min(hxforplt95))
xmax=max(max(hxforplt95),max(hxforplt5))
ymin=min(min(hyforplt5),min(hyforplt95))
ymax=max(max(hyforplt5),max(hyforplt95))
print("wwww",xmax-xmin,ymax-ymin)
print(max(hyforplt95)-min(hyforplt95),max(hxforplt95)-min(hxforplt95))
plt.figure(1)
# plt.axis([1000, -500, -500, 1000)

plt.scatter(hxforplt5, hyforplt5,label="5%",marker="+")
plt.scatter(hxforplt95, hyforplt95,label="95%",marker=".")
plt.legend()
plt.savefig(r"..\pyactrforstoptrain\4400.png")
plt.show()