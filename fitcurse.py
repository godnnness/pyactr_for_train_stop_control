# /usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import xlrd
with open("chunk.csv", "w") as f:
    workbook = xlrd.open_workbook(r'..\pyactrforstoptrain\s-d1.xlsx')
    booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
    carspeed, dangwei, tuijianspeed, dis_juli = [], [], [], []
    for i in booksheet.col_values(2):
        # print("iiiiiiiiiiii", i)
        dangwei.append(int(i))
    for i in booksheet.col_values(0):
        carspeed.append(round(i, 1))
    for i in booksheet.col_values(1):
        tuijianspeed.append(round(i, 1))
    for i in booksheet.col_values(4):
        dis_juli.append(round(i, 1))
# print(dis_juli)
# print(tuijianspeed)
#定义x、y散点坐标
# x = [10,20,30,40,50,60,70,80]
tuijianspeed = np.array(tuijianspeed)
# print('tuijianspeed is :\n',tuijianspeed)
# num = [174,236,305,334,349,351,342,323]
dis_juli = np.array(dis_juli)
# print('dis_juli is :\n',dis_juli)
#用3次多项式拟合
f1 = np.polyfit(dis_juli,tuijianspeed, 2)
print('f1 is :\n',f1)
p1 = np.poly1d(f1)
print('p1 is :\n',p1)
#也可使用yvals=np.polyval(f1, x)
yvals = p1(dis_juli) #拟合y值
# print('yvals is :\n',yvals)
#绘图
plot1 = plt.plot(dis_juli, tuijianspeed, 's',label='original values')
plot2 = plt.plot(dis_juli, yvals, 'r',label='polyfit values')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=4) #指定legend的位置右下角
plt.title('polyfitting')
plt.show()
