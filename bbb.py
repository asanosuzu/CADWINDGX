# coding=utf-8
# coding=GBK
# 入此门者，当放弃一切希望
from numpy import *
import numpy as np
import math
from math import *
import os
from scipy.optimize import curve_fit as fit
import numpy as nmp
from scipy.optimize import leastsq
from scipy import integrate
from scipy import interpolate as syip
from matplotlib import pyplot as plt
from numpy import *
from scipy import interpolate
from scipy.optimize import curve_fit as fit
from math import *
# import sympy
from scipy import integrate
import os
from scipy.optimize import leastsq


def yitihuaChaiFen(dataa):
    a = dataa
    Line = zeros((1, 4))
    Aa = zeros((len(a), 4))
    for i in range(len(a)):  # 循环赋值
        Line0 = a[i].split()
        Aa[i][0] = float(Line0[0])
        Aa[i][1] = float(Line0[1]) / 2  # 将文件中的直径值转换为半径值
        Aa[i][2] = abs(float(Line0[2]))
        Aa[i][3] = float(Line0[3])
    Aa = Aa[Aa[:, 0].argsort()]  # 按照第1列对行排序
    # Rmax = max(Aa[0:, 1])  # 获取最大值
    # tmin = min(Aa[0:, 3])  # 获取最小值
    # c = np.where(Aa == max(Aa[0:, 1]))  # 获取直径最大值所在行号和列号，即是筒身段的直径值
    # return [Aa,c,Rmax,tmin]
    return [Aa]


def yitihuaDataSolve(datab):
    chaifen0 = yitihuaChaiFen(datab)  # 拆分出各个值
    Aa = chaifen0[0]

    # 预定义
    # 轮廓绘制用
    X = []
    R = []
    alpha = []
    h = []
    # 角度和厚度用
    X11 = []
    R11 = []
    alpha11 = []
    h11 = []

    # 循环赋值
    for i1 in range(len(Aa)):
        # 画轮廓
        X.append(Aa[i1][0])
        R.append(Aa[i1][1])  # 半径值，文件里面是直径值，已在拆分函数里面转换为半径
        # alpha.append(Aa[i1][2]);
        # h.append(Aa[i1][3]);

        # 赋角度和厚度
        # if Aa[i1][2]>0:#只提取一个循环的数据
        #     X11.append(Aa[i1][0]);
        #     R11.append(Aa[i1][1]);  # 半径值，文件里面是直径值，已在拆分函数里面转换为半径
        #     alpha11.append(Aa[i1][2]);
        #     h11.append(Aa[i1][3]);

        # 输出全部厚度
        X11.append(Aa[i1][0])
        R11.append(Aa[i1][1])  # 半径值，文件里面是直径值，已在拆分函数里面转换为半径
        alpha11.append(Aa[i1][2])
        h11.append(Aa[i1][3])

    # 获取重复值行号
    hanghao = []
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
    i = 0
    for num in hanghao:
        num = num - i
        i = i + 1
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

    weizhi = np.where(X11 <= max(X))
    # weizhi=max([i for i in range(len(X11)) if X11[i]<=X[weizhi[-1]]])
    X11 = X11[0:weizhi[0][-1] + 1]
    R11 = R11[0:weizhi[0][-1] + 1]
    alpha11 = alpha11[0:weizhi[0][-1] + 1]
    h11 = h11[0:weizhi[0][-1] + 1]

    return [X, R, X11, R11, alpha11, h11]  # X11,alpha11原始LAM文件位置角度


# 基函数值递归计算
def yitihuacoxDeBoor(u, knots, ii, k):
    # Test for end conditions
    if k == 0:
        if knots[ii] <= u < knots[ii + 1]:
            return 1
        return 0
    Den1 = knots[ii + k] - knots[ii]
    Den2 = knots[ii + k + 1] - knots[ii + 1]
    Eq1 = 0
    Eq2 = 0
    if Den1 > 0:
        Eq1 = ((u - knots[ii]) / Den1) * yitihuacoxDeBoor(u, knots, ii, (k - 1))
    if Den2 > 0:
        Eq2 = ((knots[ii + k + 1] - u) / Den2) * yitihuacoxDeBoor(u, knots, (ii + 1), (k - 1))

    return Eq1 + Eq2


# 厚度光滑性处理
def yitihuasmooth(H):
    H1 = H[:]
    # 2020.11.6先来一个简单粗暴的处理，取两点平均
    j = 0
    for ii in arange(1, len(H1) - 1, 1):
        H1[ii] = (H1[ii - 1] + H1[ii + 1]) / 2
        j = ii
    H1[j + 1] = (H1[j - 1] + H1[j]) / 2
    H1[0] = (H1[0] + H1[1]) / 2
    # 得到内部跳跃的最大差值
    maxtiaoyuechazhi0 = max([H1[i + 1] - H1[i] for i in range(len(H1) - 1)])
    a = 20
    tiaoyue = [maxtiaoyuechazhi0]
    houducha = []
    xielv0 = []
    for ii in arange(0, a, 1):
        for ii in arange(1, len(H1) - 1, 1):
            H1[ii] = (H1[ii - 1] + H1[ii + 1]) / 2
        H1[ii + 1] = (H1[ii - 1] + H1[ii]) / 2
        H1[0] = (H1[0] + H1[1]) / 2
        maxtiaoyuechazhi1 = max([H1[i + 1] - H1[i] for i in range(len(H1) - 1)])
        tiaoyue.append(maxtiaoyuechazhi1)
        chazhi = [abs(H1[i] - H[i]) for i in range(len(H1))]
        zuidazhi = max(chazhi)
        houducha.append(zuidazhi)
        xyz = [tiaoyue[i + 1] / houducha[i] for i in range(len(tiaoyue) - 1)]

    return H1


# 基函数计算
def b_spline_basis(i, k, u, nodeVector):
    # nodeVector = np.mat(nodeVector)  # 将输入的节点转化成能够计算的数组
    # k=0时，定义一次基函数
    if k == 0:
        if (nodeVector[i] <= u) & (u <= nodeVector[i + 1]):  # 若u在两个节点之间，函数之为1，否则为0
            result = 1
        else:
            result = 0
    else:
        length1 = nodeVector[i + k] - nodeVector[i]
        length2 = nodeVector[i + k + 1] - nodeVector[i + 1]
        if length1 == 0:  # 特别定义 0/0 = 0
            alpha = 0
        else:
            alpha = (u - nodeVector[i]) / length1
        if length2 == 0:
            beta = 0
        else:
            beta = (nodeVector[i + k + 1] - u) / length2
        # 递归定义
        result = alpha * b_spline_basis(i, k - 1, u, nodeVector) + beta * b_spline_basis(i + 1, k - 1, u, nodeVector)
    return result


# 画B样条函数图像/均匀节点向量
def draw_b_spline(k, X, Y, nn):
    n = len(X)
    nodeVector = [0] * k + list(range(n - k)) + [n - k] * (1 + k)

    nj = 10 * nodeVector[-1]
    basis_i = np.zeros(nj)  # 存放第i个基函数
    rx = np.zeros(nj)  # 存放B样条的横坐标
    ry = np.zeros(nj)
    nodeVector = np.array(nodeVector)
    for ii in range(n):  # 计算第i个B样条基函数，
        U = np.linspace(nodeVector[k], nodeVector[n], nj)  # 在节点向量收尾之间取100个点，u在这些点中取值
        j = 0
        for u in U:
            basis_i[j] = b_spline_basis(ii, k, u, nodeVector)  # 计算取u时的基函数的值
            j = j + 1
        rx = rx + X[ii] * basis_i
        ry = ry + Y[ii] * basis_i
    # -----------------------------------------

    LLL = [0] * len(rx)
    xy = 0
    for ii in range(len(rx) - 1):  # 计算总长度
        lll = ((rx[ii + 1] - rx[ii]) ** 2 + (ry[ii + 1] - ry[ii]) ** 2) ** 0.5
        xy += lll
        LLL[ii + 1] = xy
    S = LLL[-1]
    a = S / (nn - 1)
    xy = a
    nrx = [0] * nn
    nry = [0] * nn
    for ii in range(nn - 1):  # 按比例生成均匀点列表

        for j in range(len(rx) - 1):
            if (xy >= LLL[j]) & (xy < LLL[j + 1]):
                nrx[ii + 1] = (rx[j + 1] - rx[j]) * (xy - LLL[j]) / (LLL[j + 1] - LLL[j]) + rx[j]
                nry[ii + 1] = (ry[j + 1] - ry[j]) * (xy - LLL[j]) / (LLL[j + 1] - LLL[j]) + ry[j]
                break
        xy += a
    nrx[0] = rx[0]
    nry[0] = ry[0]
    nrx[-1] = rx[-1]
    nry[-1] = ry[-1]
    return nrx, nry


# 用户定义数据
R0_jikong1 = 20
R0_jikong2 = 20
tschangdu = 600
n0 = 60  # 左封头分段数
n02 = 60  # 右封头分段数
guodujuli = 20

# 程序自定义数据
# Lunkuox = [[zuo] [zhong] [you]]
Lunkuox = []
Lunkuoy = []
Alpha = []

# ---------------------------------------------------

# 读取数据文件
path = "E:\\CADWINDGX\\qipin101"  # 待读取的文件夹
path_list = os.listdir(path)
path_list1 = list()
for filename in path_list:
    path_list1.append(os.path.join(path, filename))
    print(os.path.join(path, filename))

CiShu = [(0, 'a', 0.0, 0.0, 0.0, 0.0, 0.0)] * len(path_list)  # 创建二维列表

for iij in range(len(path_list1)):
    Lam1 = open(path_list1[iij], 'r')
    data1 = Lam1.readlines()
    Lam1.close()
    del (data1[0:2])  # 删除前面的两行非数值项,Cadwind默认生成的非数据行
    paixu = yitihuaChaiFen(data1)
    TSbanjing = max(list(paixu[0][:, 1]), key=list(paixu[0][:, 1]).count)  # 拆分数据便于排序
    tsind = list(paixu[0][:, 1]).index(TSbanjing)
    TShoudu = min(paixu[0][:, 3])  # 拆分数据便于排序
    a1min = paixu[0][tsind, 2]
    length = len(paixu[0][:, 1])
    ZJKbanjing = min(list(paixu[0][:int(length / 2), 1]))
    YJKbanjing = min(list(paixu[0][int(length / 2):, 1]))

    if a1min > 89:
        crfs = 'hoop'
    else:
        crfs = 'helix'
    CiShu[iij] = (iij, crfs, TSbanjing, TShoudu, a1min, ZJKbanjing, YJKbanjing)

CiShu.sort(key=(lambda b: b[2]))  # 按筒身半径排序
# CiShu00 = CiShu[:]
# j = 0
# for ijj in range(len(CiShu00) - 1):
#     if CiShu00[ijj + 1][2] - CiShu00[ijj][2] >= 1.2 * CiShu00[ijj][3]:
#         CiShu.insert(ijj + 1 + j, 'Hoop')
#         j = j + 1

print(CiShu)

qianhoop = 0  # 最内层环向数
for i in range(len(CiShu)):
    if CiShu[i][1] == 'hoop':
        qianhoop = i + 1
    else:
        break

# 生成内轮廓：组合内轮廓/全内轮廓
ZJKs = [i[5] for i in CiShu]
YJKs = [i[6] for i in CiShu]

for ii in range(qianhoop, len(CiShu)):
    if CiShu[ii][1] == 'helix':
        Lam1 = open(path_list1[CiShu[ii][0]], 'r')  # 按照内外层定的顺序读取文件
        data1 = Lam1.readlines()
        Lam1.close()
        del (data1[0:2])  # 删除前面的两行非数值项,Cadwind默认生成的非数据行
        data = yitihuaDataSolve(data1)
        # 绘制轮廓用
        X1 = data[0]
        R1 = data[1]

        # 角度赋予用
        X12 = data[2]
        R12 = data[3]
        alpha1 = data[4]
        h1 = data[5]
        plt.plot(X12,R12,'*-')
plt.axis("equal")
plt.show()

