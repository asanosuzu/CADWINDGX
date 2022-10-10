# -*- coding: mbcs -*-
# -*- coding: utf-8 -*-
from numpy import *
import numpy as nmp
from scipy.integrate import odeint


from math import *

import os
import math

from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
import numpy as np
from scipy import integrate
import sketch



# 下面是一体化的
######################################################################################################################



# 自定义数据处理相关函数
#声明自定义函数
def yitihuaChaiFen(data):
    a = data
    Line = zeros((1, 4))
    Aa = zeros((len(a), 4))
    for i in range(len(a)):  # 循环赋值
        Line0 = a[i].split()
        Aa[i][0] = float(Line0[0])
        Aa[i][1] = float(Line0[1])/2#将文件中的直径值转换为半径值
        Aa[i][2] = float(Line0[2])
        Aa[i][3] = float(Line0[3])
    Aa = Aa[Aa[:, 0].argsort()]  # 按照第1列对行排序
       # Rmax = max(Aa[0:, 1])  # 获取最大值
    # tmin = min(Aa[0:, 3])  # 获取最小值
    # c = np.where(Aa == max(Aa[0:, 1]))  # 获取直径最大值所在行号和列号，即是筒身段的直径值
    # return [Aa,c,Rmax,tmin]
    return [Aa]

# def yitihuaDataSolve(data,changdu,fengtoucha):
def yitihuaDataSolve(data):
    chaifen0=yitihuaChaiFen(data)#拆分出各个值
    Aa=chaifen0[0]

#预定义
    # 轮廓绘制用
    X =[]
    R =[]
    alpha =[]
    h = []
    # 角度和厚度用
    X11 = []
    R11 = []
    alpha11 = []
    h11 = []

#循环赋值
    for i1 in range(len(Aa)):
        # 画轮廓
        X.append(Aa[i1][0]);
        R.append(Aa[i1][1]);#半径值，文件里面是直径值，已在拆分函数里面转换为半径
        # alpha.append(Aa[i1][2]);
        # h.append(Aa[i1][3]);

        # 赋角度和厚度
        # if Aa[i1][2]>0:#只提取一个循环的数据
        #     X11.append(Aa[i1][0]);
        #     R11.append(Aa[i1][1]);  # 半径值，文件里面是直径值，已在拆分函数里面转换为半径
        #     alpha11.append(Aa[i1][2]);
        #     h11.append(Aa[i1][3]);

        # 输出全部厚度
        X11.append(Aa[i1][0]);
        R11.append(Aa[i1][1]);  # 半径值，文件里面是直径值，已在拆分函数里面转换为半径
        alpha11.append(Aa[i1][2]);
        h11.append(Aa[i1][3]);

# 获取重复值行号
    hanghao= []
    for ii1 in range(len(Aa) - 1):
        if Aa[ii1 + 1][0] == Aa[ii1][0] and abs(Aa[ii1 + 1][2]) == abs(Aa[ii1][2]):  # 位同角同(取绝对值)
            hanghao.append(ii1)
        else:
            pass
        if Aa[ii1 + 1][0] == Aa[ii1][0] and abs(Aa[ii1 + 1][2]) != abs(Aa[ii1][2]):  # 位同角不同(取绝对值)
            hanghao.append(ii1)
        else:
            pass

    hanghao1 = []
    for ii1 in range(len(X11) - 1):
        if X11[ii1 + 1] == X11[ii1] and abs(alpha11[ii1 + 1]) == abs(alpha11[ii1]):  # 位同角同(取绝对值)
            hanghao1.append(ii1)
        else:
            pass
        if X11[ii1 + 1] == X11[ii1] and abs(alpha11[ii1 + 1]) != abs(alpha11[ii1]):  # 位同角不同(取绝对值)
            hanghao1.append(ii1)
        else:
            pass

# 去除重复坐标值
    i=0
    for num in hanghao:
        num=num-i
        i=i+1
        del (X[num])
        del (R[num])
        # del (alpha[num])
        # del (h[num])
    i = 0
    for num in hanghao1:
        num = num - i
        i = i + 1
        del (X11[num])
        del (R11[num])
        del (alpha11[num])
        del (h11[num])

# 2020.8.23改，用总长来限定这里的尾部下降段
#     weizhi=[i for i in range(len(X)) if X[i]>(changdu-fengtoucha) and (R[i]-R[i-1])<0]
#     X=X[0:weizhi[0]]
#     R=R[0:weizhi[0]]


    weizhi=np.where(X11<=max(X))
    # weizhi=max([i for i in range(len(X11)) if X11[i]<=X[weizhi[-1]]])
    X11 = X11[0:weizhi[0][-1]+1]
    R11 = R11[0:weizhi[0][-1]+1]
    alpha11 = alpha11[0:weizhi[0][-1]+ 1]
    h11 = h11[0:weizhi[0][-1] + 1]

    return [X,R,X11,R11,alpha11,h11]###X11,alpha11原始LAM文件位置角度


 #BSpline3次
# degree. 3次样条
    # 第一步：设置曲线次数为p = 3，读取控制顶点P0, P1, ...Pn，根据控制顶点得到节点向量U = {u0, u1....um}，注意m = n + p + 1.
    # 为了保证拟合的曲线经过第一个、最后一个控制点，节点向量首末重复度要设置为为p + 1，即U = {0, 0, 0, 0, u(4)...u(n), 1, 1, 1, 1}
    # 第二步：按照本文描述的DeBoor算法完成递推函数
    # 第三步：在0 ≤ u ≤ 1取值，即可得到u对应的P(u)位置
# 规范化初始弧长
def yitihuaguifanhua(CPointX, CPointY):
    knotType = 1  # knot的计算方式 0：平均取值  1：根据长度取值
    k = 3
    n = len(CPointX)
    knot = list(nmp.arange(n + k + 1))  # 创建首末控制点重度，便于曲线过端点控制点
    for i in range(0, 4):  # 由B样条性质构建左右数据控制点的k+1重节点，k为基函数阶数
        knot[i] = 0.0
        knot[n + i] = 1.0
    if knotType:
        L = list(nmp.arange(n - 1))
        S = 0
        for i in range(n - 1):  # 计算矢量长
            L[i] = nmp.sqrt(pow(CPointX[i + 1] - CPointX[i], 2) + pow(CPointY[i + 1] - CPointY[i], 2))
            S = S + L[i]
        tmp = L[0]
        for i in range(4, n):  # 按矢量比例均分，曲线定义域内
            tmp = tmp + L[i - 3]
            knot[i] = tmp / S
    else:
        tmp = 1 / (float(n) - 3)  # 因为三次样条是4个节点一个曲线段，现在在将曲线定义域用n-k来均分定义区间
        tmpS = tmp
        for i in range(4, n):
            knot[i] = tmpS
            tmpS = tmpS + tmp
    return knot
# 基函数值递归计算
def yitihuacoxDeBoor(u, knots, i, k):
    # Test for end conditions
    if (k == 0):
        if (knots[i] <= u and u < knots[i + 1]):
            return 1
        return 0
    Den1 = knots[i + k] - knots[i]
    Den2 = knots[i + k + 1] - knots[i + 1]
    Eq1 = 0;
    Eq2 = 0;
    if Den1 > 0:
        Eq1 = ((u - knots[i]) / Den1) * yitihuacoxDeBoor(u, knots, i, (k - 1))
    if Den2 > 0:
        Eq2 = ((knots[i + k + 1] - u) / Den2) * yitihuacoxDeBoor(u, knots, (i + 1), (k - 1))

    return Eq1 + Eq2
# 生成Bspline点坐标，并修正R值
def yitihuaB3Spline(CPointX,CPointY,knot,Bsjindu):
    BsplineX = []
    BsplineY = []
    for ip in range(len(CPointX) - 3):  # 创建B样条
        u = linspace(knot[ip + 3], knot[ip + 4], Bsjindu)  # 节点区间值
        for j in arange(len(u)):  # 创建均B样条
            BsplineX.append(
                CPointX[ip] * yitihuacoxDeBoor(u[j], knot, ip, 3) + CPointX[ip + 1] * yitihuacoxDeBoor(u[j], knot, ip + 1, 3) \
                + CPointX[ip + 2] * yitihuacoxDeBoor(u[j], knot, ip + 2, 3) + CPointX[ip + 3] * yitihuacoxDeBoor(u[j], knot, ip + 3,
                                                                                                   3))
            BsplineY.append(
                CPointY[ip] * yitihuacoxDeBoor(u[j], knot, ip, 3) + CPointY[ip + 1] * yitihuacoxDeBoor(u[j], knot, ip + 1, 3) \
                + CPointY[ip + 2] * yitihuacoxDeBoor(u[j], knot, ip + 2, 3) + CPointY[ip + 3] * yitihuacoxDeBoor(u[j], knot, ip + 3,
                                                                                                   3))
    # 2020.8.30改
    # 会导致出现点过原点的错误
    if BsplineX[-1] == 0:
        del BsplineX[-1]
        del BsplineY[-1]
    # 到尾喷管端点
    BsplineX.append(CPointX[-1])
    BsplineY.append(CPointY[-1])
    # plt.plot(BsplineX, BsplineY, '-r')
    # plt.plot([BsplineX[0], BsplineX[-1]], [0, 0], 'g')
    # plt.plot([BsplineX[0], BsplineX[-1]], [R0_jikong, R0_jikong], 'b')
    # plt.plot(CPointX, CPointY, '-ob', label="Waypoints")
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()
    return [BsplineX,BsplineY]

#通过厚度求取外轮廓，即是通过两个数据点的向量值夹角和厚度值反求对应的外轮廓点
def yitihuawailunkuo1(X,R,H):
    X2wai = []
    R2wai = []

# 第一个数据点位的厚度反算轮廓
    theta = math.atan(-(X[1] - X[0]) / (R[1] - R[0]))
    Delta_X = (2 * H[0]) * cos(theta)
    Delta_R = (2 * H[0]) * sin(theta)
    X2wai.append(X[0] - Delta_X)
    R2wai.append(R[0] - Delta_R)

# 除第一个数据点外的数据点位厚度反算轮廓
#     2020.10.1改
    for i111 in range(len(X) - 1):
        i111 = i111 + 1
        theta=math.atan(-(R[i111]-R[i111-1])/(X[i111]-X[i111-1]))
        Delta_X=(2*H[i111])*sin(theta)
        Delta_R=(2*H[i111])*cos(theta)
        if R[i111]>R[i111-1]:
            X2wai.append(X[i111]+Delta_X)
            R2wai.append(R[i111]+Delta_R)
        if R[i111]<R[i111-1]:
            X2wai.append(X[i111]+Delta_X)
            R2wai.append(R[i111]+Delta_R)
        if R[i111]==R[i111-1]:
            X2wai.append(X[i111])
            R2wai.append(R[i111]+ 2*H[i111])
    # plt.plot(X2wai,R2wai,'g')
    # plt.show()
    return [X2wai,R2wai]

#通过厚度求取外轮廓，即是通过两个数据点的向量值夹角和厚度值反求对应的外轮廓点
#左封头
def yitihuawailunkuozuo(X,R,H,tsX):
    X2_zuo_wai = list()
    R2_zuo_wai = list()
    # if X[0]!=max(X):
    #     X=X[::-1]#因为以赤道圆作为初始位置，需翻转左封头的数据
    #     R=R[::-1]
    #     H=H[::-1]
    X2_zuo_wai.append(tsX[0])
    R2_zuo_wai.append(max(R)+2*H[0])
    for i111 in range(len(X) - 1):
        i111 = i111 + 1
        theta=math.atan(-(X[i111]-X[i111-1])/(R[i111]-R[i111-1]))
        Delta_X=(2*H[i111])*cos(theta)
        Delta_R=(2*H[i111])*sin(theta)
        X2_zuo_wai.append(X[i111]-Delta_X)
        R2_zuo_wai.append(R[i111]-Delta_R)
    # plt.plot(X2_zuo_wai,R2_zuo_wai)
    return [X2_zuo_wai,R2_zuo_wai]

#右封头
def yitihuawailunkuoyou(X,R,H,tsX):
    X2_you_wai = list()
    R2_you_wai = list()

    X2_you_wai.append(tsX[1])
    R2_you_wai.append(max(R)+ 2*H[0])
    for i222 in range(len(X) - 1):
        i222 = i222 + 1

        theta = math.atan(-(R[i222] - R[i222 - 1]) / (X[i222] - X[i222 - 1]))
        Delta_X = (2 * H[i222]) * sin(theta)
        Delta_R = (2 * H[i222]) * cos(theta)
        if R[i222] > R[i222 - 1]:
            X2_you_wai.append(X[i222] + Delta_X)
            R2_you_wai.append(R[i222] + Delta_R)
        if R[i222] < R[i222 - 1]:
            X2_you_wai.append(X[i222] + Delta_X)
            R2_you_wai.append(R[i222] + Delta_R)
        if R[i222] == R[i222 - 1]:
            X2_you_wai.append(X[i222])
            R2_you_wai.append(R[i222] + 2 * H[i222])
            R2_you_wai.append(R[i222] + 2 * H[i222])

#         k1=-(X[i222] - X[i222 - 1]) / (R[i222] - R[i222 - 1])
#         theta=math.atan(k1)
#         Delta_X=(2*H[i222])*cos(theta)
#         if k1>=0:
#             Delta_R=(2*H[i222])*sin(theta)
#         if k1<0:#喉颈部位以后的厚度反推计算
#             Delta_R = -(2 * H[i222]) * sin(theta)
# # 一体化独有
#         if R[i222]>R[i222-1]:
#             X2_you_wai.append(X[i222]-Delta_X)
#             R2_you_wai.append(R[i222]+Delta_R)
#         if R[i222]<R[i222-1]:
#             X2_you_wai.append(X[i222]+Delta_X)
#             R2_you_wai.append(R[i222]+Delta_R)
#         if R[i222]==R[i222-1]:
#             X2_you_wai.append(X[i222])
#             R2_you_wai.append(R[i222]+ 2*H[i222])
    # plt.plot(X2_you_wai,R2_you_wai,'r')
    # plt.show()
    return [X2_you_wai,R2_you_wai]

def yitihuaXiuZheng(x,X,R):#R坐标修正
    # 修正半径值,因为X/Y坐标是一一对应的，所以可以找到离x坐标最近的那个R作为我的现在的修正的R,为后面厚度反推外轮廓做准备
    Rxiuzh = []
    Xxiuzh = []
    Hxiuzh = []
    for i in range(len(x)):
        jdz = [abs(X[j] - x[i]) for j in range(len(X))]  # 绝对值
        c1 = jdz.index(min(jdz))  # 获取各个x对应为修正位置
        Xxiuzh.append(X[c1])
        Rxiuzh.append(R[c1])
    return [Xxiuzh,Rxiuzh]

def yitihuahoudupingwen(X,R,pingwenxishu,tsX):#前后前跳动值平稳处理，用来为轮廓生成做准备
    # 两个向量夹角判定
    j=0
    weizhi=[]
    for i in range(len(X) - 2):
        axaingliang=[X[i+1-j]-X[i-j],R[i+1-j]-R[i-j]]#a向量
        bxaingliang=[[X[i+2-j]-X[i+1-j]],[R[i+2-j]-R[i+1-j]]]#b向量
        amochang=((X[i+1-j]-X[i-j])**2+(R[i+1-j]-R[i-j])**2)**0.5#模长
        bmochang=((X[i+2-j]-X[i+1-j])**2+(R[i+2-j]-R[i+1-j])**2)**0.5#模长
        alp=(math.acos((np.dot(axaingliang,bxaingliang)) / (amochang* bmochang)))*180/math.pi
        if abs(alp)>pingwenxishu*180/math.pi and X[i-j]>tsX[1]:#去除急转的角度相邻位置值
            weizhi.append(i+2)#将波动位置存储起来后面统一删除
        if abs(alp)>pingwenxishu*180/math.pi and X[i-j]<tsX[0]:#去除急转的角度相邻位置值
            weizhi.append(i+2)#将波动位置存储起来后面统一删除
    for ii in range(len(weizhi)):
        del (X[weizhi[ii]-j])
        del (R[weizhi[ii]-j])
        j+=1

    return [X,R]

def yitihuaQujiange(old_listX,old_listR,shuliang):
    new_listX = []
    new_listR = []
    new_listX.append(old_listX[0])
    new_listR.append(old_listR[0])
    # 获取平均距离
    distance = [((old_listX[i] - old_listX[i + 1]) ** 2 + (old_listR[i] - old_listR[i + 1]) ** 2) ** 0.5 for i in
               range(len(old_listX) - 1)]
    pingjudistance = sum(distance) / shuliang
    i = 0
    for j in range(1, len(old_listX)):
        if ((old_listX[j] - old_listX[i]) ** 2 + (old_listR[j] - old_listR[i]) ** 2) ** 0.5 > pingjudistance:
            new_listX.append(old_listX[j - 1])
            new_listR.append(old_listR[j - 1])
            i = j
    # new_list=old_list[0:len(old_list):inter]
    if new_listX[-1] != old_listX[-1] or new_listR[-1] != old_listR[-1]:
        new_listX.append(old_listX[-1])
        new_listR.append(old_listR[-1])
    else:
        pass
    return [new_listX, new_listR]

# 2020.8.23修正增加，这里的x会出现相等的情况必须再次去重处理
def yitihuaquchong(X,R,H,alpha1):
    weizhi=[i for i in range(len(X)) if X[0:i+1].count(X[i])>1]# 找到去除X重复项的位置
    for i in range(len(weizhi)):
        del (X[weizhi[i]-i])
        del (R[weizhi[i]-i])
        del (H[weizhi[i]-i])
        del (alpha1[weizhi[i]-i])
    return [X,R,H,alpha1]

# 厚度光滑性处理
def yitihuasmooth(H):
    x=arange(0,len(H),1)
    # plt.plot(x,H,'-r')
    H1=H[:]
    # 2020.11.6先来一个简单粗暴的处理，取两点平均
    for i in arange(1,len(H1)-1,1):
        H1[i]=(H1[i-1]+H1[i+1])/2
    H1[i+1]=(H1[i-1]+H1[i])/2
    H1[0]=(H1[0]+H1[1])/2
    # 得到内部跳跃的最大差值
    maxtiaoyuechazhi0=max([H1[i+1]-H1[i] for i in range(len(H1)-1)])
    a=20
    tiaoyue=[]
    tiaoyue.append(maxtiaoyuechazhi0)
    houducha=[]
    xielv0 = []
    for i in arange(0, a, 1):
        for i in arange(1, len(H1) - 1, 1):
            H1[i] = (H1[i - 1] + H1[i + 1]) / 2
        H1[i + 1] = (H1[i - 1] + H1[i]) / 2
        H1[0] = (H1[0] + H1[1]) / 2
        maxtiaoyuechazhi1 = max([H1[i + 1] - H1[i] for i in range(len(H1) - 1)])
        tiaoyue.append(maxtiaoyuechazhi1)
        chazhi = [abs(H1[i] - H[i]) for i in range(len(H1))]
        zuidazhi = max(chazhi)
        houducha.append(zuidazhi)
        xyz = [tiaoyue[i + 1] / houducha[i] for i in range(len(tiaoyue) - 1)]
        if i > 0:
            xielv = (xyz[i] - xyz[i - 1]) / 1#通过斜率控制，刚开始下降比较快，后面就没必要了，误差还大
            xielv0.append(xielv)
            if abs(xielv) < 2e-3:
                break
    # plt.plot(arange(0, len(H1), 1),H1, '-b')
    # # plt.plot(arange(0, len(tiaoyue), 1), tiaoyue, '-b')
    # # plt.plot(arange(1, len(houducha) + 1, 1), houducha, '-r')
    # # plt.plot(arange(1, len(xyz) + 1, 1), xyz, '-g')
    # plt.grid(True)
    # plt.legend()
    # # plt.axis("equal")
    # plt.show()

    return H1






######################################################################################################################

# def yitihua(fileName,layup,E1,E2,E3,G12,G13,G23,Nu12,Nu13,Nu23,pressure,hxdt,
        # R0_jikong,R0_weipenguan,changdu,fengtoucha,youfengtou,tschangdu,zhuanjiao,jinshunei):
def yitihua(fileName,layup,E1,E2,E3,G12,G13,G23,Nu12,Nu13,Nu23,pressure,hxdt,changdu,tschangdu,zhuanjiao,jinshunei):
    print(layup)
    # print(E1,E2,E3,G12,G13,G23,Nu12,Nu13,Nu23,pressure,hxdt,\
        # R0_jikong,R0_weipenguan,changdu,fengtoucha,youfengtou,tschangdu,zhuanjiao,jinshunei)
    print(E1,E2,E3,G12,G13,G23,Nu12,Nu13,Nu23,pressure,hxdt,changdu,tschangdu,zhuanjiao,jinshunei)

    # 导入相关的cadwind数据
    # 读取数据文件
    Lam1 = open(fileName, 'r')
    data1 = Lam1.readlines()
    Lam1.close()
    del (data1[0:2])  # 删除前面的两行非数值项,Cadwind默认生成的非数据行


    ######################################################################################################################


    puceng=[]

    for x in layup:
        puceng.append(x[0])



    engineeringdata=(E1,E2,E3,Nu12,Nu13,Nu23,G12,G13,G23)

    #默认参数不需要插件输入
    #Bsjindu=BsplinePrecision#B样条单个区间拟合精度
    # todegree=pi/180.0
    # jiangeshu=internalNum#绘制三维模型间隔取点数量
    # pingwenxishu=smoothCoefficient#外轮廓相邻点平稳系数，越小越平稳，太小会出问题，需适当调节

    Bsjindu=20#B样条单个区间拟合精度
    zhuanjiao=30.0#三维实体模型的转角
    todegree=pi/180.0
    pingwenxishu=0.15#外轮廓相邻点平稳系数，越小越平稳，太小会出问题，需适当调节


    ######################################################################################################################


    # 初始化数据存储参数
    # 端点值
    # 左
    XddianZ=[]
    RddianZ=[]
    # 右
    XddianY=[]
    RddianY=[]

    # 轮廓
    # 内表面
    neisX=[]
    neisR=[]
    # 外表面
    waisX=[]
    waisR=[]

    ######################################################################################################################


     # 得到传入处理后的初步数据
    #内表面
    # 得到最内层的轮廓和螺旋缠绕的角度数据
    # 得到各个数据值
    # data=yitihuaDataSolve(data1,changdu,fengtouchazuo)
    data=yitihuaDataSolve(data1)
    #绘制轮廓用
    X1=data[0]
    R1=data[1]
    # 角度赋予用
    X12=data[2]
    R12=data[3]
    alpha1=data[4]
    h1=data[5]


    ######################################################################################################################


    # 2020.11.7
    # 极孔线性外插
    # 左
    x1=X12[0]
    x2=X12[1]

    y1=R12[0]
    y2=R12[1]

    Y=np.array([[y1],[y2]])
    mat2=np.array([[x1,1],[x2,1]])
    mat2 = np.mat(mat2)
    mat3 = mat2.I#求逆
    xishu=mat3*Y
    zuojikquzhengX=-ceil(abs(X12[0]))
    zuojikquzhengR=round(xishu[0,0]*zuojikquzhengX+xishu[1,0])

    R0_jikong=zuojikquzhengR
    fengtouchazuo=abs(zuojikquzhengX)#左封头长度

    # 去除尾部下降段
    j=0
    for i in range(len(X1)):
        if X1[i-j]>changdu-fengtouchazuo:
            del (X1[i-j])
            del (R1[i-j])
            del (X12[i-j])
            del (R12[i-j])
            del (alpha1[i-j])
            del (h1[i-j])
            j+=1

    ######################################################################################################################


    # 根据两边极孔条件删除不在范围内的点
    weizhi00=[i for i in range(len(R12)) if R12[i]<=R0_jikong and X12[i]<0]
    j=0
    for i in range(len(weizhi00)):
        del (X12[weizhi00[i-j]])
        del (R12[weizhi00[i-j]])
        del (alpha1[weizhi00[i-j]])
        del (h1[weizhi00[i-j]])
        j+=1
    aa=[i for i in range(len(X12)) if X12[i]<=0]
    if aa[-1]!=0:
        X12[aa[-1]]=0
        R12[aa[-1]]=R12[aa[-1]+1]

    ######################################################################################################################


    # # 对厚度进行平稳处理，便于后面轮廓的光滑
    h1=yitihuasmooth(h1)

    CPointX=[]
    CPointY=[]
    # 用B样条拟合外轮廓
    CPointX = X1[:]  # 整理B样条需要数据
    CPointY = R1[:]
    # 根据两边极孔条件删除不在范围内的点
    weizhi00=[i for i in range(len(CPointY)) if CPointY[i]<=R0_jikong and CPointX[i]<0]
    j=0
    for i in range(len(weizhi00)):
        del (CPointX[weizhi00[i-j]])
        del (CPointY[weizhi00[i-j]])
        j+=1

    ######################################################################################################################


    # 右侧插入控制点减缓曲线突变程度
    p=20#插入控制点数量
    qujian=20
    for i in range(qujian):
        for j in arange(1,p,1):
            [CPointX.insert(-(p*i+j),X1[-(i+1)]-j*(X1[-(i+1)]-X1[-(i+2)])/p)]
            [CPointY.insert(-(p*i+j),R1[-(i+1)]-j*(R1[-(i+1)]-R1[-(i+2)])/p)]


    ######################################################################################################################


    # 得到B样条的数据点
    knot = yitihuaguifanhua(CPointX[:], CPointY[:])  # 生成B样条节点
    B3 = yitihuaB3Spline(CPointX[:], CPointY[:], knot[:],Bsjindu)  # 得到B样条数据点

    # 2020.9.19改
    BsplineX = B3[0][:]
    BsplineY = B3[1][:]
    x1 = BsplineX[0] + (R0_jikong - BsplineY[1]) * ((BsplineX[0] - BsplineX[1]) / (BsplineY[0] - BsplineY[1]))
    BsplineX.insert(0, x1)
    BsplineY.insert(0, R0_jikong)
    B3[0][:] = BsplineX
    B3[1][:] = BsplineY


    ######################################################################################################################

    # 内轮廓
    neisX=B3[0][:]
    neisR=B3[1][:]
    # plt.plot(neisX,neisR)
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()
    # 端点
    # 左
    XddianZ.append(B3[0][0])
    RddianZ.append(B3[1][0])
    # 右
    XddianY.append(B3[0][-1])
    RddianY.append(B3[1][-1])


    ######################################################################################################################


    #外表面
    # 得到螺旋缠绕的外表面轮廓数据
    # 修正现在的X,R值，用B样条中的离该点X坐标最近的那个数据点代替原始X,R值
    cc = yitihuaXiuZheng(X12, B3[0], B3[1])
    xiuzX = cc[0][:]
    xiuzR = cc[1][:]


    bb=yitihuaquchong(xiuzX[:], xiuzR[:], h1[:],alpha1[:])
    xiuzX =bb[0][:]
    xiuzR = bb[1][:]
    h1= bb[2][:]
    alpha1= bb[3][:]


    ######################################################################################################################


    # 得到环向层的厚度之后加入到螺旋层的筒身厚度计算中去
    huanxsl=puceng.count('Hoop')
    tshouduhx=huanxsl*hxdt
    # 螺旋总厚度
    luoxuansl=puceng.count('HelixLoop')
    h2=[i*luoxuansl for i in h1]


    ######################################################################################################################


    # 后面需要处理的厚度
    XX11=[]
    RR11=[]
    # 找出筒身的位置
    tsX=[]
    tsR=[]
    XX =fengtouchazuo  ###左边封头位置
    zuotongshen=0
    jdz = [abs(B3[0][j] - XX) for j in range(len(B3[0]))]  # 绝对值
    weizhi1=jdz.index(min(jdz))  # 获取各个x对应为修正位置
    #得到左部赤道圆位置坐标
    # tsX.append(B3[0][weizhi1])
    # tsR.append(B3[1][weizhi1])
    tsX.append(0)
    tsR.append(B3[1][weizhi1])

    # 提取筒身螺旋单层厚度/角度
    weizhi=[i for i in range(len(xiuzX)) if 0<xiuzX[i]<tschangdu]
    lxdt=h1[(weizhi[0]+weizhi[-1])/2]
    luoxuanjiao=abs(alpha1[(weizhi[0]+weizhi[-1])/2])

    # 得到右部赤道圆位置坐标
    XX =tsX[0] + tschangdu     #####右边赤道圆位置
    youtongshen=tsX[0]
    jdz = [abs(B3[0][j] - XX) for j in range(len(B3[0]))]  # 绝对值
    weizhi2=jdz.index(min(jdz))  # 获取各个x对应为修正位置
    # tsX.append(B3[0][weizhi2])
    tsR.append(B3[1][weizhi2])
    tsX.append(tsX[0] + tschangdu)
    # tsR.append(tsR[0])#保证两侧赤道圆直径相等

    # 左
    a=[xiuzX[i] for i in range(len(xiuzX)) if xiuzX[i]<tsX[0] and xiuzX[i]<0]
    b=[xiuzR[i] for i in range(len(xiuzX)) if xiuzX[i]<tsX[0] and xiuzX[i]<0]
    c=[h2[i] for i in range(len(xiuzX)) if xiuzX[i]<tsX[0] and xiuzX[i]<0]
    X=list(reversed(a))
    R=list(reversed(b))
    H1=list(reversed(c))
    waizuo=yitihuawailunkuozuo(X,R,H1,tsX)#得到极孔处修正的外轮廓，删掉了一部分厚度
    Xzuo=list(reversed(waizuo[0]))
    Rzuo=list(reversed(waizuo[1]))
    Hzuo=list(reversed(H1))
    j=0
    for i in range(len(Xzuo)):
        if Xzuo[i-j] <X[0]-fengtouchazuo-lxdt*luoxuansl*max(Rzuo)/R0_jikong:#长度限定,对内外轮廓多做截断处理
            #外部
            del(Xzuo[i-j])
            del(Rzuo[i-j])
            del(Hzuo[i-j])
            del(a[i-j])
            del(b[i-j])
            j+=1
        if Xzuo[i-j]>tsX[0]:
            del (Xzuo[i - j])
            del (Rzuo[i - j])
            del (Hzuo[i - j])
            del (a[i - j])
            del (b[i - j])
            j += 1
    [XX11.append(a[i]) for i in range(len(a)) if (a[i]<=max(Xzuo)) and (a[i]>=min(Xzuo))]
    [RR11.append(b[i]) for i in range(len(a)) if (a[i]<=max(Xzuo)) and (a[i]>=min(Xzuo))]
    ############################################################
    # 得到右部赤道圆位置坐标
    XX =tsX[0] + tschangdu     #####右边赤道圆位置
    youtongshen=XX
    jdz = [abs(B3[0][j] - XX) for j in range(len(B3[0]))]  # 绝对值
    weizhi2=jdz.index(min(jdz))  # 获取各个x对应为修正位置
    # tsX.append(B3[0][weizhi2])
    # tsR.append(B3[1][weizhi2])

    # 右
    X=[xiuzX[i] for i in range(len(xiuzX)) if xiuzX[i]>tsX[1]]
    R=[xiuzR[i] for i in range(len(xiuzX)) if xiuzX[i]>tsX[1]]
    Hyou=[h2[i] for i in range(len(xiuzX)) if xiuzX[i]>tsX[1]]
    waiyou=yitihuawailunkuoyou(X,R,Hyou,tsX)#得到极孔处修正的外轮廓，删掉了一部分厚度
    Xyou=waiyou[0]
    Ryou=waiyou[1]
    j=0
    for i in range(len(Xyou)):
        if Xyou[i-j] >changdu-abs(min(Xzuo)):#长度限定
           # 外部
            del (Xyou[i - j])
            del (Ryou[i - j])
            del (Hyou[i - j])
            del (X[i - j])
            del (R[i - j])
            j += 1
        if Xyou[i-j]<tsX[1]:
            del (Xyou[i - j])
            del (Ryou[i - j])
            del (Hyou[i - j])
            del (X[i - j])
            del (R[i - j])
            j += 1
    # 筒身数据
    [XX11.append(xiuzX[i]) for i in range(len(xiuzX)) if (xiuzX[i]>=tsX[0]) and (xiuzX[i]<=tsX[1])]
    [RR11.append(xiuzR[i]) for i in range(len(xiuzX)) if (xiuzX[i]>=tsX[0]) and (xiuzX[i]<=tsX[1])]
    # 右封头
    [XX11.append(X[i]) for i in range(len(X)) if (X[i]>=min(Xyou)) and (X[i]<=max(Xyou))]
    [RR11.append(R[i]) for i in range(len(X)) if (X[i]>=min(Xyou)) and (X[i]<=max(Xyou))]


    ######################################################################################################################


    # 删除掉极孔处有问题的数据点之后，重新组装新的外部轮廓数据
    #重新定义新的厚度数据，保护原始数据
    X11=[]
    R11=[]
    H11=[]

    #左封头数据
    [X11.append(i) for i in Xzuo]
    [R11.append(i) for i in Rzuo]
    [H11.append(i) for i in Hzuo]

    #筒身数据
    for i in range(len(xiuzX)):
        if xiuzX[i]<=tsX[1] and xiuzX[i]>=tsX[0]:
            X11.append(xiuzX[i])
            R11.append(xiuzR[i])#一体化的半径有的时候两侧半径大小不一问题，后面可能会出错
            # R11.append(tsR[0]+tshouduhx)
            # H11.append(h2[i])
            H11.append(lxdt*luoxuansl)

    #右封头数据
    [X11.append(i) for i in Xyou]
    [R11.append(i) for i in Ryou]
    [H11.append(i) for i in Hyou]


    ######################################################################################################################


    # 做赤道圆的过渡处理
    # 2020.9.22
    # 在赤道圆过渡位置寻找使其与封头相切的位置近似点
    leftTransitionX=tsX[0]
    leftTransitionR=tsR[0]+lxdt*luoxuansl*2+tshouduhx
    rightTransitionX=tsX[1]
    rightTransitionR=tsR[0]+lxdt*luoxuansl*2+tshouduhx
    tangentlineL=[]
    tangentlineR=[]
    wz=[]
    for i in range(len(X11)):
        if X11[i]<leftTransitionX:
            tangentlineL.append(math.atan(((X11[i] -leftTransitionX) / (R11[i] -leftTransitionR)))*180/math.pi)
        if X11[i] > rightTransitionX:
            tangentlineR.append(math.atan(((X11[i] -rightTransitionX)/(R11[i] - rightTransitionR)))*180/math.pi)
        if (X11[i] <= rightTransitionX) and (X11[i]>=leftTransitionX):
            wz.append(i)
    wz1=tangentlineL.index(max(tangentlineL))
    # wz2=tangentlineR.index(min(tangentlineR))
    # 2020.11.7
    pp=[]
    for i in range(len(tangentlineR)-1):
        xielv=tangentlineR[i+1]-tangentlineR[i]
        pp.append(xielv)
        if xielv>0:
            break
    wz2=i
    # 左
    for num in arange(wz1,min(wz)-1,1):
        t1=(tshouduhx)/(leftTransitionX-X11[wz1])*(X11[num]-X11[wz1])
        H11[num]=H11[num]+t1*0.5

    # 右
    for num in arange(max(wz)+1,max(wz)+1+wz2,1):
        t1=(tshouduhx)/(rightTransitionX-X11[max(wz)+1+wz2])*(X11[num]-X11[max(wz)+1+wz2])
        H11[num]=H11[num]+t1*0.5

    # 筒身部分环向层做加上环向层厚度的处理
    for num in arange(min(wz)-1,max(wz)+1,1):
        H11[num]=H11[num]+tshouduhx*0.5


    ######################################################################################################################


    # 对厚度光滑处理减缓厚度突变
    Hh=H11
    # Hh=yitihuasmooth(H11)#光滑处理一下
    Xnei=[]
    Rnei=[]
    for ii in range(len(XX11)):#通过内部轮廓数据截断外部X两侧，后面做修正处理
        if XX11[ii]<=max(X11) and XX11[ii]>=min(X11):
            Xnei.append(XX11[ii])
            Rnei.append(RR11[ii])
    try:
        wailunkuo = yitihuawailunkuo1(Xnei[:], Rnei[:], Hh[:])
    except:
        print("the wailunkuo command have problem")
        # 去除掉外轮廓x坐标在内轮廓横坐标控制范围外的点
    # for i in  range(len(wailunkuo[0])):
    #     plt.plot((Xnei[i],wailunkuo[0][i]),(Rnei[i],wailunkuo[1][i]),'-b')
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()

    j=0
    for ii in range(len(wailunkuo[0][:])):
        if wailunkuo[0][ii-j]<min(Xnei[:]) or  wailunkuo[0][ii-j]>max(Xnei[:]):
            del(wailunkuo[0][ii-j])
            del(wailunkuo[1][ii-j])
            j += 1
    WX = wailunkuo[0][:]
    WR = wailunkuo[1][:]

    # plt.plot(WX,WR)
    # plt.plot(Xnei,Rnei)
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()


    ######################################################################################################################


    # 厚度平稳处理
    # 左封头
    xzuo=[WX[i] for i in range(len(WX[:])) if WX[i]<=tsX[0]]
    rzuo=[WR[i] for i in range(len(WX[:])) if WX[i]<=tsX[0]]
    chuli=yitihuahoudupingwen(xzuo[::-1],rzuo[::-1],pingwenxishu,tsX)
    WXzuo = chuli[0][::-1]
    WRzuo = chuli[1][::-1]
    # 筒身
    WXzhong=[WX[i] for i in range(len(WX[:])) if tsX[0]<WX[i]<tsX[1]]
    WRzhong=[WR[i] for i in range(len(WX[:])) if tsX[0]<WX[i]<tsX[1]]
    # 右封头
    xyou=[WX[i] for i in range(len(WX[:])) if WX[i]>=tsX[1]]
    ryou=[WR[i] for i in range(len(WX[:])) if WX[i]>=tsX[1]]
    chuli=yitihuahoudupingwen(xyou[:],ryou[:],pingwenxishu,tsX)
    WX = WXzuo+WXzhong+chuli[0][:]
    WR = WRzuo+WRzhong+chuli[1][:]

    # plt.plot(WX,WR,'*r')
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()


    ######################################################################################################################


    # 这里的抛物线修正
    # 左侧
    zuoX11=min(neisX)-Hzuo[0]#左边极孔纤维堆积后的坐标
    # 最后两点的切线值
    Kk=(WX[0]-WX[1])/(WR[0]-WR[1])
    aa=(WX[0]-zuoX11-Kk*(WR[0]-R0_jikong))/(((WR[0]**2-R0_jikong**2))-2*WR[0]*(WR[0]-R0_jikong))
    bb=Kk-2*aa*WR[0]
    cc=zuoX11-aa*R0_jikong**2-bb*R0_jikong
    XXjikongzuo=[]
    RRjikongzuo=[]
    for i in arange(R0_jikong,WR[0],0.05):#靠近极孔这边的抛物线修正
        XXjikongzuo.append(aa*i**2+bb*i+cc)
        RRjikongzuo.append(i)
    WX=XXjikongzuo+WX
    WR=RRjikongzuo+WR

    # plt.plot(WX,WR)
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()


    ######################################################################################################################


    # 进行平稳处理
    pingwen=yitihuahoudupingwen(WX,WR,pingwenxishu,tsX)
    # 用B样条拟合外轮廓
    CPointX = pingwen[0][:]  # 整理B样条需要数据
    CPointY = pingwen[1][:]

    # 2020.10.1改，右侧没到最右端处理
    if CPointX[-1]<neisX[-1]:
        CPointX.append(neisX[-1])
        # CPointY.append(neisR[-1]+Hh[-1])
        # 通过斜率插入
        xielv=(CPointY[-2]-CPointY[-1])/(CPointX[-3]-CPointX[-2])
        y0=-xielv*(CPointX[-2]-CPointX[-1])+CPointY[-1]
        CPointY.append(y0)


    # 一体化独有
    # 厚度反推后存在x交错情况，可以通过判定x值调整
    j=0
    for i in range(len(CPointX)-1):
        if CPointX[i+1-j]<CPointX[i-j]:
            del(CPointX[i+1-j])
            del(CPointY[i+1-j])
            j+=1


    # # 2020.10.1改,加密控制顶点
    # 右侧插入控制点减缓曲线突变程度
    p=20#插入控制点数量
    qujian=20
    xzuo = CPointX[:]
    xyou = CPointX[:]
    yzuo = CPointY[:]
    yyou = CPointY[:]
    for i in range(qujian):

        for j in arange(1,p,1):

            [CPointX.insert(-(p*i+j),xyou[-(i+1)]-j*(xyou[-(i+1)]-xzuo[-(i+2)])/p)]
            [CPointY.insert(-(p*i+j),yyou[-(i+1)]-j*(yyou[-(i+1)]-yzuo[-(i+2)])/p)]


    ######################################################################################################################


    # 对赤道圆处的赤道数据轮廓不明显采取的赤道圆加密数据处理，得到合适赤道圆数据
    # 筒身赤道处加密数据控制点，减少这里的变化突变
    # 找到赤道圆在控制点中的位置
    where1=[i for i in range(len(CPointX)-1) if CPointX[i]<=tsX[0] and tsX[0]<=CPointX[i+1]]#左赤道圆
    where2=[i for i in range(len(CPointX)-1) if CPointX[i]<=tsX[1] and tsX[1]<=CPointX[i+1]]#右赤道圆
    CPointX.insert(where1[0]+1,tsX[0])#扩充赤道圆值
    CPointY.insert(where1[0]+1,CPointY[where1[0]+1])#扩充赤道圆值
    CPointX.insert(where2[0]+2,tsX[1])
    CPointY.insert(where2[0]+2,CPointY[where2[0]+1])#扩充赤道圆值
    where1=[i for i in range(len(CPointX)) if CPointX[i]==tsX[0]]#左赤道圆
    where2=[i for i in range(len(CPointX)) if CPointX[i]==tsX[1]]#右赤道圆


    ######################################################################################################################


    # 赤道圆过度处加密
    p=5
    qujian=[where1[0],where2[0]]
    for i in qujian:
        if i==qujian[0]:
            for j in arange(1,p,1):
                [CPointX.insert((i+1),CPointX[(i)]+j*(CPointX[(i+1)]-CPointX[(i)])/p)]
                [CPointY.insert((i+1),CPointY[(i+1)])]
        if i == qujian[1]:
            for j in arange(1, p, 1):
                [CPointX.insert((i +p-1), CPointX[(i +p-1)]-j * (CPointX[(i + p-1)] - CPointX[(i+p-2)]) / p)]
                [CPointY.insert((i +p-1), CPointY[(i - 2+p)])]

    # plt.plot(CPointX,CPointY)
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()


    ######################################################################################################################


    # 生成外轮廓B样条节点
    knot = yitihuaguifanhua(CPointX[:], CPointY[:])  # 生成B样条节点
    B3 = yitihuaB3Spline(CPointX[:], CPointY[:], knot[:],Bsjindu)  # 得到B样条数据点
    # 2020.9.19改
    BsplineX=B3[0][:]
    BsplineY=B3[1][:]
    x1 = BsplineX[0] + (R0_jikong - BsplineY[1]) * ((BsplineX[0] - BsplineX[1]) / (BsplineY[0] - BsplineY[1]))
    BsplineX.insert(0,x1)
    BsplineY.insert(0,R0_jikong)
    # 2020.10.1改，右侧没到最右端处理
    if BsplineX[-1]<neisX[-1]:
        BsplineX.append(neisX[-1])
        BsplineY.append(BsplineY[-1])


    ######################################################################################################################


    # 得到外轮廓绘制图形数据
    waisX=BsplineX
    waisR=BsplineY
    # plt.plot(waisX,waisR)
    # plt.plot(neisX,neisR)
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()
    # 端点
    # 左
    XddianZ.append(waisX[0])
    RddianZ.append(waisR[0])
    # 右
    XddianY.append(B3[0][-1])
    RddianY.append(B3[1][-1])


    # 从B样条数据里面取一部分，防止导入abaqus卡死
    neisXR=yitihuaQujiange(neisX,neisR,len(X12))
    neisX=neisXR[0][:]
    neisR=neisXR[1][:]

    waisXR=yitihuaQujiange(waisX,waisR,len(X12))
    waisX=waisXR[0][:]
    waisR=waisXR[1][:]


    # plt.plot(neisX,neisR,'*y')
    # plt.plot(waisX,waisR,'*b')
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.show()
    #
    # plt.plot(neisX,neisR,'-y')
    # plt.plot(waisX,waisR,'-b')


    # 绘图
    # plt.show()


    ######################################################################################################################


    # 二、下面是abaqus分析模块


    ######################################################################################################################


    # abaqus建模
    #引入abaqus模块建模
    # #导入abaqus模块
    # from abaqus import *
    # from abaqusConstants import *
    # from caeModules import *
    # import sketch

    Mdb()#创建新的模型数据库
    modelName = 'composite'
    m = mdb.Model(name=modelName)


    #在abaqus中绘制草图
    session.viewports['Viewport: 1'].view.fitView()
    s1 = m.ConstrainedSketch(name='composite-'+str('huojianfadongjiketi'), sheetSize=2*int(waisX[-1]))
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    constructionline=s1.ConstructionLine(point1=(waisX[0], 0), point2=(waisX[-1], 0))  # 根据外层X坐标自动调整轴线长度
    s1.assignCenterline(line=constructionline)
    s1.FixedConstraint(entity=constructionline)
    Vline=s1.ConstructionLine(point1=(0.0, -20.0), point2=(0.0, max(waisR)))
    s1.FixedConstraint(entity=Vline)


    ######################################################################################################################


    j=0
    for i in range(1,len(waisX)-2):
        if waisX[i+1-j]<tsX[0] and waisX[i-j]>min(Xnei[:]):
            if (waisX[i+1-j]-waisX[i-j])**2+(waisR[i+1-j]-waisR[i-j])**2<1:#距离太近的清除掉,防止后面abaqus的B样条畸形
                del(waisX[i-j])
                del(waisR[i-j])
                j += 1
        if waisX[i+1-j]>tsX[1] and waisX[i+1-j]<max(Xnei[:]):
            if (waisX[i+1-j]-waisX[i-j])**2+(waisR[i+1-j]-waisR[i-j])**2<1:
                del(waisX[i+1-j])
                del(waisR[i+1-j])
                j += 1


    ######################################################################################################################

    # 绘制轮廓草图
    Spoints1 = zip(neisX[:], neisR[:])#打包坐标点
    curve1 = s1.Spline(points=Spoints1)
    Spoints2 = zip(waisX[:], waisR[:])#打包坐标点
    curve2 = s1.Spline(points=Spoints2)
    line_cy5 = s1.Line(point1=(XddianZ[0], RddianZ[0]),
                       point2=(XddianZ[1], RddianZ[1]))  # 端点的存储没有区分纯螺旋与非纯螺旋
    line_cy6 = s1.Line(point1=(XddianY[0], RddianY[0]),
                       point2=(XddianY[1], RddianY[1]))
    s1 = mdb.models[modelName].ConstrainedSketch(name='__edit__', 
        objectToCopy=mdb.models[modelName].sketches['composite-'+str('huojianfadongjiketi')])
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)


