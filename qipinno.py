# coding=utf-8
# coding=GBK
"""
‘入此门者，当放弃一切希望’——但丁
插件建模思路：
1、文件处理、得到CiShu列表 √
2、得到起始内轮廓，均匀间隔数据点 √
3、循环lam文件得到各层轮廓点数据以及角度数据 √
4、根据环向位置生成中间轮廓数据、根据环向起始位置更新左右轮廓数据
5、添加补强，更新左右轮廓数据点
6、后处理
"""
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


# 基函数计算
def b_spline_basis(ik, k, u, nodeVector):
    # nodeVector = np.mat(nodeVector)  # 将输入的节点转化成能够计算的数组
    # k=0时，定义一次基函数
    if k == 0:
        if (nodeVector[ik] <= u) & (u <= nodeVector[ik + 1]):  # 若u在两个节点之间，函数之为1，否则为0
            result = 1
        else:
            result = 0
    else:
        length1 = nodeVector[ik + k] - nodeVector[ik]
        length2 = nodeVector[ik + k + 1] - nodeVector[ik + 1]
        if length1 == 0:  # 特别定义 0/0 = 0
            alpha = 0
        else:
            alpha = (u - nodeVector[ik]) / length1
        if length2 == 0:
            beta = 0
        else:
            beta = (nodeVector[ik + k + 1] - u) / length2
        # 递归定义
        result = alpha * b_spline_basis(ik, k - 1, u, nodeVector) + beta * b_spline_basis(ik + 1, k - 1, u, nodeVector)
    return result


# 画B样条函数图像/均匀节点向量
def draw_b_spline(kk, X, Y, nn):
    n = len(X)
    nodeVector = [0] * kk + list(range(n - kk)) + [n - kk] * (1 + kk)

    nj = 10 * nodeVector[-1]
    basis_i = np.zeros(nj)  # 存放第i个基函数
    rx = np.zeros(nj)  # 存放B样条的横坐标
    ry = np.zeros(nj)
    nodeVector = np.array(nodeVector)
    for it in range(n):  # 计算第i个B样条基函数，
        U = np.linspace(nodeVector[kk], nodeVector[n], nj)  # 在节点向量收尾之间取100个点，u在这些点中取值
        jt = 0
        for u in U:
            basis_i[jt] = b_spline_basis(it, kk, u, nodeVector)  # 计算取u时的基函数的值
            jt = jt + 1
        rx = rx + X[it] * basis_i
        ry = ry + Y[it] * basis_i
    # -----------------------------------------
    LLL = [0] * len(rx)
    xy = 0
    for it in range(len(rx) - 1):  # 计算总长度
        lll = ((rx[it + 1] - rx[it]) ** 2 + (ry[it + 1] - ry[it]) ** 2) ** 0.5
        xy += lll
        LLL[it + 1] = xy
    S = LLL[-1]
    a = S / (nn - 1)
    xy = a
    nrx = [0] * nn
    nry = [0] * nn
    for it in range(nn - 1):  # 按比例生成均匀点列表

        for jt in range(len(rx) - 1):
            if (xy >= LLL[jt]) & (xy < LLL[jt + 1]):
                nrx[it + 1] = (rx[jt + 1] - rx[jt]) * (xy - LLL[jt]) / (LLL[jt + 1] - LLL[jt]) + rx[jt]
                nry[it + 1] = (ry[jt + 1] - ry[jt]) * (xy - LLL[jt]) / (LLL[jt + 1] - LLL[jt]) + ry[jt]
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
tschangdu = 600  # 筒身长度
n0 = 100  # 左封头分段数
n02 = 100  # 右封头分段数
guodugrid = 6  # 扩孔平滑过渡的分片数
guodugrid2 = 4  # 环向过渡段分片数
guodugrid3 = 4  # 补强过渡段分片数
# buqiangtable = ((0, -50, -30, 45, 0.6, 'AL6061', 'windReinforce'), (1, -42, -20, 30, 0.6, 'AL6061', 'windReinforce'),
#                 (0, -6, 601, 90, 0.5, 'AL6061', 'windReinforce'), (0, 620, 648, 30, 0.6), (1, 630, 652, 30, 0.6),
#                 (2, 10, 590, 90, 0.5))  # 左封头补强、右封头补强、环向层
buqiangtable = ()
# 程序自定义数据

# ---------------------------------------------------
# 一、读取数据文件，生成CiShu列表
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

LAMx = []
LAMy = []
# ------------------------------------------------------------------------------------------------------------
# 二、生成内轮廓：组合内轮廓/全内轮廓  ！第二层必须是不扩孔
qianhoop = 0  # 最内层环向数
for i in range(len(CiShu)):
    if CiShu[i][1] == 'hoop':
        qianhoop = i + 1
    else:
        break

ZJKs = [i[5] for i in CiShu]
YJKs = [i[6] for i in CiShu]
if CiShu[qianhoop][5] == min(ZJKs) and CiShu[qianhoop][6] == min(YJKs):  # 首层不扩孔，全内轮廓
    # ---处理首个螺旋层
    Lam1 = open(path_list1[CiShu[qianhoop][0]], 'r')  # 按照内外层定的顺序读取文件
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
    LAMx.append(X12)
    LAMy.append(R12)
    # 提取左封头数据
    aa = [i for i in range(len(X12)) if X12[i] <= 0]  # 取X=0
    if aa[-1] != 0:
        X12[aa[-1]] = 0
        R12[aa[-1]] = R12[aa[-1] + 1]  # 让封头上最后两个点半径相等，做平滑处理
    Xzuo = [X12[i] for i in aa]
    Rzuo = [R12[i] for i in aa]
    Azuo = [abs(alpha1[i]) for i in aa]
    Hzuo = [h1[i] for i in aa]

    # 提取右封头数据
    aa = [i for i in range(len(X12)) if X12[i] >= tschangdu]  # 取X=tschangdu
    if aa[0] != tschangdu:
        X12[aa[0]] = tschangdu
        R12[aa[0]] = R12[aa[0] - 1]  # 让封头上最前两个点半径相等，做平滑处理
    Xyou = [X12[i] for i in aa]
    Ryou = [R12[i] for i in aa]
    Ayou = [abs(alpha1[i]) for i in aa]
    Hyou = [h1[i] for i in aa]

    # 筒身数据
    aa = [i for i in range(len(X12)) if 0 < X12[i] < tschangdu]
    Rzhong = sum([R12[i] for i in aa[1:len(aa) - 1]]) / (len(aa) - 2)
    Azhong = sum([abs(alpha1[i]) for i in aa[1:len(aa) - 1]]) / (len(aa) - 2)
    Hzhong = sum([abs(h1[i]) for i in aa[1:len(aa) - 1]]) / (len(aa) - 2)

    # ###########左封头B样条拟合内轮廓、角度、厚度，反推外轮廓##################################################
    if 1:
        # 取一半控制点
        if len(Xzuo) % 2:
            XXzuo = Xzuo[::2]
            RRzuo = Rzuo[::2]
        else:
            XXzuo = Xzuo[::2]
            XXzuo.append(Xzuo[-1])
            RRzuo = Rzuo[::2]
            RRzuo.append(Rzuo[-1])

        # #轮廓处理
        k0 = 3
        XzuoB, YzuoB = draw_b_spline(k0, Xzuo, Rzuo, n0)

    # ###########右封头B样条拟合内轮廓、角度、厚度，反推外轮廓##################################################
    if 1:
        # 取一半控制点
        if len(Xyou) % 2:
            XXyou = Xyou[::2]
            XXyou.insert(1, Xyou[1])
            RRyou = Ryou[::2]
            RRyou.insert(1, Ryou[1])
            AAyou = Ayou[::2]
            AAyou.insert(1, Ayou[1])
        else:
            XXyou = Xyou[::2]
            XXyou.insert(1, Xyou[1])
            XXyou.append(Xyou[-1])
            RRyou = Ryou[::2]
            RRyou.insert(1, Ryou[1])
            RRyou.append(Ryou[-1])
            AAyou = Ayou[::2]
            AAyou.insert(1, Ayou[1])
            AAyou.append(Ayou[-1])

        k0 = 3
        XyouB, YyouB = draw_b_spline(k0, XXyou, RRyou, n02)

else:  # 首层即扩孔，组合内轮廓:左边首层扩、右边首层扩、两边首层扩
    print('首层即扩孔')
    Lam1 = open(path_list1[CiShu[qianhoop][0]], 'r')  # 按照内外层定的顺序读取文件
    data1 = Lam1.readlines()
    Lam1.close()
    del (data1[0:2])  # 删除前面的两行非数值项,Cadwind默认生成的非数据行
    data = yitihuaDataSolve(data1)
    # 绘制轮廓用
    X12 = data[2]
    R12 = data[3]
    LAMx.append(X12)
    LAMy.append(R12)
    # 提取左封头数据
    aa = [i for i in range(len(X12)) if X12[i] <= 0]  # 取X=0
    if aa[-1] != 0:
        X12[aa[-1]] = 0
        R12[aa[-1]] = R12[aa[-1] + 1]  # 让封头上最后两个点半径相等，做平滑处理
    Xzuo = [X12[i] for i in aa]
    Rzuo = [R12[i] for i in aa]

    # 提取右封头数据
    aa = [i for i in range(len(X12)) if X12[i] >= tschangdu]  # 取X=tschangdu
    if aa[0] != tschangdu:
        X12[aa[0]] = tschangdu
        R12[aa[0]] = R12[aa[0] - 1]  # 让封头上最前两个点半径相等，做平滑处理
    Xyou = [X12[i] for i in aa]
    Ryou = [R12[i] for i in aa]

    # 左内轮廓
    if CiShu[0][5] == min(ZJKs):  # 左边首层不扩孔
        print('左边首层不扩孔')
        # #轮廓处理
        k0 = 3
        XzuoB, YzuoB = draw_b_spline(k0, Xzuo, Rzuo, n0)
    else:  # 左边首层扩孔
        indz = ZJKs.index(min(ZJKs))
        Lam1 = open(path_list1[CiShu[indz][0]], 'r')  # 按照内外层定的顺序读取文件
        data1 = Lam1.readlines()
        Lam1.close()
        del (data1[0:2])  # 删除前面的两行非数值项,Cadwind默认生成的非数据行
        data = yitihuaDataSolve(data1)
        # 绘制轮廓用
        X12 = data[2]
        R12 = data[3]

        # 提取左封头数据
        aa = [i for i in range(len(X12)) if X12[i] <= 0]  # 取X=0
        if aa[-1] != 0:
            X12[aa[-1]] = 0
            R12[aa[-1]] = R12[aa[-1] + 1]  # 让封头上最后两个点半径相等，做平滑处理
        Xzuo2 = [X12[i] for i in aa]
        Rzuo2 = [R12[i] for i in aa]
        Xzuo2 = Xzuo2[Rzuo2.index(min(Rzuo2)):]  # 只取单调增部分
        Rzuo2 = Rzuo2[Rzuo2.index(min(Rzuo2)):]  # 只取单调增部分

        # 找出内轮廓部分数据，结合形成完整内轮廓
        Rzuomin = Rzuo[0]
        XXzuo = []
        RRzuo = []
        for i in range(len(Rzuo2)):
            if Rzuo2[i] < Rzuomin:
                XXzuo.append(Xzuo2[i])
                RRzuo.append(Rzuo2[i])

        Xzuo = XXzuo + Xzuo
        Rzuo = RRzuo + Rzuo

        # #轮廓处理
        k0 = 3
        XzuoB, YzuoB = draw_b_spline(k0, Xzuo, Rzuo, n0)

    # 右内轮廓
    if CiShu[0][6] == min(YJKs):  # 右边首层不扩孔
        # #轮廓处理
        k0 = 3
        XyouB, YyouB = draw_b_spline(k0, Xyou, Ryou, n02)
    else:  # 右边首层扩孔
        indy = YJKs.index(min(YJKs))
        Lam1 = open(path_list1[CiShu[indy][0]], 'r')  # 按照内外层定的顺序读取文件
        data1 = Lam1.readlines()
        Lam1.close()
        del (data1[0:2])  # 删除前面的两行非数值项,Cadwind默认生成的非数据行
        data = yitihuaDataSolve(data1)
        # 绘制轮廓用
        X12 = data[2]
        R12 = data[3]

        # 提取右封头数据
        aa = [i for i in range(len(X12)) if X12[i] >= tschangdu]  # 取X=tschangdu
        if aa[0] != tschangdu:
            X12[aa[0]] = tschangdu
            R12[aa[0]] = R12[aa[0] - 1]  # 让封头上最前两个点半径相等，做平滑处理
        Xyou2 = [X12[i] for i in aa]
        Ryou2 = [R12[i] for i in aa]
        Xyou2 = Xyou2[:Ryou2.index(min(Ryou2)) + 1]  # 只取单调增部分
        Ryou2 = Ryou2[:Ryou2.index(min(Ryou2)) + 1]  # 只取单调增部分

        # 找出内轮廓部分数据，结合形成完整内轮廓
        Ryoumin = Ryou[-1]
        XXyou = []
        RRyou = []
        for i in range(len(Ryou2)):
            if Ryou2[i] < Ryoumin:
                XXyou.append(Xyou2[i])
                RRyou.append(Ryou2[i])
        Xyou = Xyou + XXyou
        Ryou = Ryou + RRyou
        # #轮廓处理
        k0 = 3
        XyouB, YyouB = draw_b_spline(k0, Xyou, Ryou, n02)
# 保存内轮廓
NzuoX = XzuoB
NzuoY = YzuoB
NyouX = XyouB
NyouY = YyouB

# 补强用
BQNzuoX = [NzuoX]
BQNzuoY = [NzuoY]
BQNyouX = [NyouX]
BQNyouY = [NyouY]

# ----------------------------------------------------------------------------------------------------------------
# 三、循环lam文件，得到各层轮廓数据和角度数据，角度列表比轮廓列表长度小一
lunkuozuoX = []
lunkuozuoY = []
lunkuoyouX = []
lunkuoyouY = []
anglezuo = []
angleyou = []
guodugrid -= 1
parzuo = 0
paryou = 0
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
        LAMx.append(X12)
        LAMy.append(R12)
        # 左封头外轮廓以及角度
        if 1:
            # 提取左封头数据
            aa = [i for i in range(len(X12)) if X12[i] <= 0]  # 取X=0
            if aa[-1] != 0:
                X12[aa[-1]] = 0
                R12[aa[-1]] = R12[aa[-1] + 1]  # 让封头上最后两个点半径相等，做平滑处理
            Xzuo = [X12[i] for i in aa]
            Rzuo = [R12[i] for i in aa]
            Azuo = [abs(alpha1[i]) for i in aa]
            Hzuo = [h1[i] for i in aa]

            Xzuo = Xzuo[Rzuo.index(min(Rzuo)):]  # 只取lam文件单调增部分
            Azuo = Azuo[Rzuo.index(min(Rzuo)):]
            Hzuo = Hzuo[Rzuo.index(min(Rzuo)):]
            Rzuo = Rzuo[Rzuo.index(min(Rzuo)):]

            # 取一半控制点
            if len(Xzuo) % 2:
                XXzuo = Xzuo[::2]
                RRzuo = Rzuo[::2]
                AAzuo = Azuo[::2]
                HHzuo = Hzuo[::2]
            else:
                XXzuo = Xzuo[::2]
                XXzuo.append(Xzuo[-1])
                RRzuo = Rzuo[::2]
                RRzuo.append(Rzuo[-1])
                AAzuo = Azuo[::2]
                AAzuo.append(Azuo[-1])
                HHzuo = Hzuo[::2]
                HHzuo.append(Hzuo[-1])

            # 提取范围内内轮廓
            ind1 = 0
            for j in range(len(NzuoY)):
                if NzuoY[j] < Rzuo[0] <= NzuoY[j + 1]:
                    ind1 = j
                    break
                else:
                    ind1 = 0  # 不扩孔

            NNzuoX = NzuoX[ind1:]
            NNzuoY = NzuoY[ind1:]

            if ind1 > parzuo:
                parzuo = ind1
            # 拟合角度厚度
            XXzuoB, AAzuoB = draw_b_spline(k0, XXzuo, AAzuo, n0)
            func0 = syip.interp1d(XXzuoB, AAzuoB, kind='linear')
            NNzuoA1 = list(func0(NNzuoX[int(len(NNzuoY)/2):]))
            RRzuoB, AAzuoB = draw_b_spline(k0, RRzuo, AAzuo, n0)
            func0 = syip.interp1d(RRzuoB, AAzuoB, kind='linear')
            NNzuoA0 = list(func0(NNzuoY[1:int(len(NNzuoY)/2)]))
            NNzuoA = NNzuoA0 + NNzuoA1

            XXzuoB, HHzuoB = draw_b_spline(k0, XXzuo, HHzuo, n0)
            func0 = syip.interp1d(XXzuoB, HHzuoB, kind='linear')
            NNzuoH1 = list(func0(NNzuoX[int(len(NNzuoY)/2):]))

            RRzuoB, HHzuoB = draw_b_spline(k0, RRzuo, HHzuo, n0)
            func0 = syip.interp1d(RRzuoB, HHzuoB, kind='linear')
            NNzuoH0 = list(func0(NNzuoY[1:int(len(NNzuoY)/2)]))
            NNzuoH = NNzuoH0 + NNzuoH1
            # 生成外轮廓
            WWzuoX = []
            WWzuoY = []
            if ind1 > 2:  # 扩孔
                WWzuoX.append(NNzuoX[0])
                WWzuoY.append(NNzuoY[0])
                for jj in range(guodugrid, len(NNzuoX) - 2):
                    k1 = (NNzuoY[jj + 1] - NNzuoY[jj]) / (NNzuoX[jj + 1] - NNzuoX[jj])
                    k2 = (NNzuoY[jj + 2] - NNzuoY[jj + 1]) / (NNzuoX[jj + 2] - NNzuoX[jj + 1])
                    theta1 = arctan(k1) * 180 / pi
                    theta2 = arctan(k2) * 180 / pi
                    if theta1 < 0:
                        theta1 += 180
                    if theta2 < 0:
                        theta2 += 180
                    theta = (theta1 + theta2) / 2 + 90
                    WWzuoX.append(NNzuoX[jj + 1] + cos(theta / 180 * pi) * NNzuoH[jj + 1])
                    WWzuoY.append(NNzuoY[jj + 1] + sin(theta / 180 * pi) * NNzuoH[jj + 1])
                WWzuoX = list(linspace(WWzuoX[0], WWzuoX[1], guodugrid + 2)) + WWzuoX[2:]
                WWzuoY = list(linspace(WWzuoY[0], WWzuoY[1], guodugrid + 2)) + WWzuoY[2:]
                WWzuoX.append(NNzuoX[-1])
                WWzuoY.append(NNzuoY[-1] + NNzuoH[-1])
                WWzuoX[:guodugrid + 3], WWzuoY[:guodugrid + 3] = draw_b_spline(k0, WWzuoX[:guodugrid + 3],
                                                                               WWzuoY[:guodugrid + 3], guodugrid + 3)
            else:  # 不扩孔
                for jj in range(ind1 + 1):
                    k1 = (NzuoY[jj + 1] - NzuoY[jj]) / (NzuoX[jj + 1] - NzuoX[jj])
                    theta1 = arctan(k1) + pi / 2
                    WWzuoX.append(NzuoX[jj] + cos(theta1) * NNzuoH[0])
                    WWzuoY.append(NzuoY[jj] + sin(theta1) * NNzuoH[0])
                for jj in range(len(NNzuoX) - 2):
                    k1 = (NNzuoY[jj + 1] - NNzuoY[jj]) / (NNzuoX[jj + 1] - NNzuoX[jj])
                    k2 = (NNzuoY[jj + 2] - NNzuoY[jj + 1]) / (NNzuoX[jj + 2] - NNzuoX[jj + 1])
                    theta1 = arctan(k1) * 180 / pi
                    theta2 = arctan(k2) * 180 / pi
                    if theta1 < 0:
                        theta1 += 180
                    if theta2 < 0:
                        theta2 += 180
                    theta = (theta1 + theta2) / 2 + 90
                    WWzuoX.append(NNzuoX[jj + 1] + cos(theta / 180 * pi) * NNzuoH[jj + 1])
                    WWzuoY.append(NNzuoY[jj + 1] + sin(theta / 180 * pi) * NNzuoH[jj + 1])
                WWzuoX.append(NNzuoX[-1])
                WWzuoY.append(NNzuoY[-1] + NNzuoH[-1])
                WWzuoX[:parzuo + guodugrid + 3], WWzuoY[:parzuo + guodugrid + 3] \
                    = draw_b_spline(k0, WWzuoX[:parzuo + guodugrid + 3], WWzuoY[:parzuo + guodugrid + 3],
                                    parzuo + guodugrid + 3)

        # 右封头外轮廓以及角度
        if 1:
            # 提取右封头数据
            aa = [i for i in range(len(X12)) if X12[i] >= tschangdu]  # 取X=tschangdu
            if aa[0] != tschangdu:
                X12[aa[0]] = tschangdu
                R12[aa[0]] = R12[aa[0] - 1]  # 让封头上最前两个点半径相等，做平滑处理
            Xyou = [X12[i] for i in aa]
            Ryou = [R12[i] for i in aa]
            Ayou = [abs(alpha1[i]) for i in aa]
            Hyou = [h1[i] for i in aa]

            Xyou = Xyou[:Ryou.index(min(Ryou)) + 1]  # 只取lam文件单调增部分
            Ayou = Ayou[:Ryou.index(min(Ryou)) + 1]
            Hyou = Hyou[:Ryou.index(min(Ryou)) + 1]
            Ryou = Ryou[:Ryou.index(min(Ryou)) + 1]
            # 取一半控制点
            if len(Xyou) % 2:
                XXyou = Xyou[::2]
                RRyou = Ryou[::2]
                AAyou = Ayou[::2]
                HHyou = Hyou[::2]
            else:
                XXyou = Xyou[::2]
                XXyou.append(Xyou[-1])
                RRyou = Ryou[::2]
                RRyou.append(Ryou[-1])
                AAyou = Ayou[::2]
                AAyou.append(Ayou[-1])
                HHyou = Hyou[::2]
                HHyou.append(Hyou[-1])

            # 提取范围内内轮廓
            ind2 = len(NyouY) - 1
            for j in range(len(NyouY) - 1):
                if NyouY[j] >= Ryou[-1] > NyouY[j + 1]:
                    ind2 = j + 1
                    break
                else:
                    pass

            NNyouX = NyouX[:ind2 + 1]
            NNyouY = NyouY[:ind2 + 1]
            if len(NyouY) - ind2 > paryou:
                paryou = len(NyouY) - ind2
            # 拟合角度厚度
            XXyouB, AAyouB = draw_b_spline(k0, XXyou, AAyou, n02)
            func0 = syip.interp1d(XXyouB, AAyouB, kind='linear')
            NNyouA0 = func0(NNyouX[:int(len(NNyouX)/2)])

            RRyouB, AAyouB = draw_b_spline(k0, RRyou, AAyou, n02)
            func0 = syip.interp1d(RRyouB, AAyouB, kind='linear')
            NNyouA1 = func0(NNyouY[int(len(NNyouX)/2):-1])

            NNyouA = list(NNyouA0) + list(NNyouA1)

            XXyouB, HHyouB = draw_b_spline(k0, XXyou, HHyou, n02)
            func0 = syip.interp1d(XXyouB, HHyouB, kind='linear')
            NNyouH0 = func0(NNyouX[:int(len(NNyouX)/2)])

            RRyouB, HHyouB = draw_b_spline(k0, RRyou, HHyou, n02)
            func0 = syip.interp1d(RRyouB, HHyouB, kind='linear')
            NNyouH1 = func0(NNyouY[int(len(NNyouX)/2):-1])

            NNyouH = list(NNyouH0) + list(NNyouH1)
            # 生成外轮廓
            WWyouX = []
            WWyouY = []

            if ind2 < len(NyouY) - 2:  # 扩孔
                WWyouX.append(NNyouX[0])
                WWyouY.append(NNyouY[0] + NNyouH[0])
                for jj in range(len(NNyouX) - 2 - guodugrid):
                    k1 = (NNyouY[jj + 1] - NNyouY[jj]) / (NNyouX[jj + 1] - NNyouX[jj])
                    k2 = (NNyouY[jj + 2] - NNyouY[jj + 1]) / (NNyouX[jj + 2] - NNyouX[jj + 1])
                    theta1 = arctan(k1) * 180 / pi
                    theta2 = arctan(k2) * 180 / pi
                    if theta1 < 0:
                        theta1 += 180
                    if theta2 < 0:
                        theta2 += 180
                    theta = (theta1 + theta2) / 2 - 90
                    WWyouX.append(NNyouX[jj + 1] + cos(theta / 180 * pi) * NNyouH[jj + 1])
                    WWyouY.append(NNyouY[jj + 1] + sin(theta / 180 * pi) * NNyouH[jj + 1])
                WWyouX = WWyouX[:-1] + list(linspace(WWyouX[-1], NNyouX[-1], guodugrid + 2))
                WWyouY = WWyouY[:-1] + list(linspace(WWyouY[-1], NNyouY[-1], guodugrid + 2))
                WWyouX[-guodugrid - 3:], WWyouY[-guodugrid - 3:] \
                    = draw_b_spline(k0, WWyouX[-guodugrid - 3:], WWyouY[-guodugrid - 3:], guodugrid + 3)

            else:  # 不扩孔
                WWyouX.append(NNyouX[0])
                WWyouY.append(NNyouY[0] + NNyouH[0])
                for jj in range(len(NNyouX) - 2):
                    k1 = (NNyouY[jj + 1] - NNyouY[jj]) / (NNyouX[jj + 1] - NNyouX[jj])
                    k2 = (NNyouY[jj + 2] - NNyouY[jj + 1]) / (NNyouX[jj + 2] - NNyouX[jj + 1])
                    theta1 = arctan(k1) * 180 / pi
                    theta2 = arctan(k2) * 180 / pi
                    if theta1 < 0:
                        theta1 += 180
                    if theta2 < 0:
                        theta2 += 180
                    theta = (theta1 + theta2) / 2 - 90
                    WWyouX.append(NNyouX[jj + 1] + cos(theta / 180 * pi) * NNyouH[jj + 1])
                    WWyouY.append(NNyouY[jj + 1] + sin(theta / 180 * pi) * NNyouH[jj + 1])
                k1 = (NyouY[ind2] - NyouY[ind2 - 1]) / (NyouX[ind2] - NyouX[ind2 - 1])
                theta1 = arctan(k1) + pi / 2
                WWyouX.append(NyouX[ind2] + cos(theta1) * NNyouH[-1])
                WWyouY.append(NyouY[ind2] + sin(theta1) * NNyouH[-1])
                for jj in range(1, len(NyouX) - ind2):
                    k1 = (NyouY[jj + ind2] - NyouY[jj + ind2 - 1]) / (NyouX[jj + ind2] - NyouX[jj + ind2 - 1])
                    theta1 = arctan(k1) + pi / 2
                    WWyouX.append(NyouX[jj] + cos(theta1) * NNyouH[-1])
                    WWyouY.append(NyouY[jj] + sin(theta1) * NNyouH[-1])
                WWyouX[-paryou - guodugrid - 3:], WWyouY[-paryou - guodugrid - 3:] \
                    = draw_b_spline(k0, WWyouX[-paryou - guodugrid - 3:], WWyouY[-paryou - guodugrid - 3:],
                                    paryou + guodugrid + 3)
                # plt.plot(NNyouX,NNyouY,'r*-')
                # plt.plot(WWyouX, WWyouY, 'g*-')
                # plt.axis("equal")
                # plt.show()

        # 更新内轮廓
        # 左内
        if ind1 > 2:
            NzuoX = NzuoX[:ind1] + WWzuoX[:]
            NzuoY = NzuoY[:ind1] + WWzuoY[:]
        else:
            NzuoX = WWzuoX[:]
            NzuoY = WWzuoY[:]
        # 右内
        if ind2 < len(NyouY) - 2:
            NyouX = WWyouX[:] + NyouX[ind2 + 1:]
            NyouY = WWyouY[:] + NyouY[ind2 + 1:]
        else:
            NyouX = WWyouX[:]
            NyouY = WWyouY[:]

        BQNzuoX.append(NzuoX)
        BQNzuoY.append(NzuoY)
        BQNyouX.append(NyouX)
        BQNyouY.append(NyouY)
        # 本层轮廓、角度数据保存
        lunkuozuoX.append([NNzuoX, WWzuoX])
        lunkuozuoY.append([NNzuoY, WWzuoY])
        lunkuoyouX.append([NNyouX, WWyouX])
        lunkuoyouY.append([NNyouY, WWyouY])
        anglezuo.append(list(NNzuoA))
        angleyou.append(list(NNyouA))

# --------------------------------------------------------------------------------------------------
# 四、插入环向、生成中间轮廓数据、更新左右轮廓数据
'''
1、左中右轮廓合并，在插入环向层后更新轮廓
2、环向层单独建立轮廓集
'''
lunkuozhongX = []
lunkuozhongY = []
miduni = lunkuozuoX[0][0][-1] - lunkuozuoX[0][0][-2]

# #计算合适的网格数

guodugrid2 += 1
hoopnum = len([i for i in buqiangtable if i[3] == 90])
if hoopnum != 0:
    zmax = max([i[1] for i in buqiangtable if i[3] == 90])
    if zmax < 0:
        zmax = 0  # 保证环向层至少有2*guodugrid2个数据点
    ymax = tschangdu - min([i[2] for i in buqiangtable if i[3] == 90])
else:
    zmax = 0
    ymax = 0
midgrid = int(ceil(max(zmax, ymax) / miduni)) + guodugrid2

# #生成初始环向层数据
for i in range(len(lunkuozuoX)):
    lunkuozhongX.append([[], []])
    lunkuozhongY.append([[], []])
    for j in range(midgrid):
        lunkuozhongX[i][0].append(j * miduni)
        lunkuozhongX[i][1].append(j * miduni)
        lunkuozhongY[i][0].append(lunkuozuoY[i][0][-1])
        lunkuozhongY[i][1].append(lunkuozuoY[i][1][-1])
    for j in range(midgrid):
        lunkuozhongX[i][0].append(tschangdu - (midgrid - j - 1) * miduni)
        lunkuozhongX[i][1].append(tschangdu - (midgrid - j - 1) * miduni)
        lunkuozhongY[i][0].append(lunkuoyouY[i][0][0])
        lunkuozhongY[i][1].append(lunkuoyouY[i][1][0])
zhongmaxx = lunkuozhongX[0][0][midgrid - 1]

# #生成全轮廓数据
lunkuoneix = []
lunkuoneiy = []
lunkuowaix = []
lunkuowaiy = []
helix_angle = []

for i in range(len(lunkuozuoX)):
    lunkuoneix.append(lunkuozuoX[i][0] + lunkuozhongX[i][0][1:-1] + lunkuoyouX[i][0])
    lunkuoneiy.append(lunkuozuoY[i][0] + lunkuozhongY[i][0][1:-1] + lunkuoyouY[i][0])
    lunkuowaix.append(lunkuozuoX[i][1] + lunkuozhongX[i][1][1:-1] + lunkuoyouX[i][1])
    lunkuowaiy.append(lunkuozuoY[i][1] + lunkuozhongY[i][1][1:-1] + lunkuoyouY[i][1])
    ytt = (anglezuo[i][-1]+angleyou[i][0])/2
    yt = anglezuo[i]+[ytt]*(2*midgrid-1)+angleyou[i]
    helix_angle.append(yt)

huan_nx = []
huan_ny = []
huan_wx = []
huan_wy = []

for i in range(len(buqiangtable)):
    if buqiangtable[i][3] == 90 and buqiangtable[i][1] <= (tschangdu / 2) <= buqiangtable[i][2]:  # 环向
        hou = buqiangtable[i][4]
        ind3 = buqiangtable[i][0]
        # 提取环向区间
        hzs = 0
        hys = 0
        if ind3 == 0:  # 环向在最里，没有参考轮廓
            for j in range(len(lunkuoneix[0])):
                if lunkuoneix[0][j] <= buqiangtable[i][1] < lunkuoneix[0][j + 1]:
                    hzs = j
                    break
            for j in range(len(lunkuoneix[0])):
                if lunkuoneix[0][j - 1] < buqiangtable[i][2] <= lunkuoneix[0][j]:
                    hys = j
                    break
            neix = lunkuoneix[0][hzs:hys + 1]
            neiy = lunkuoneiy[0][hzs:hys + 1]
        else:
            for j in range(len(lunkuowaix[ind3 - 1])):
                if lunkuowaix[ind3 - 1][j] <= buqiangtable[i][1] < lunkuowaix[ind3 - 1][j + 1]:
                    hzs = j
                    break
            for j in range(len(lunkuowaix[ind3 - 1])):
                if lunkuowaix[ind3 - 1][j - 1] < buqiangtable[i][2] <= lunkuowaix[ind3 - 1][j]:
                    hys = j
                    break
            neix = lunkuowaix[ind3 - 1][hzs:hys + 1]
            neiy = lunkuowaiy[ind3 - 1][hzs:hys + 1]

        # 生成厚度列表
        hou0 = list(linspace(0, hou, guodugrid2))
        hou1 = list(linspace(hou, 0, guodugrid2))
        houall = hou0 + [hou] * (hys - hzs + 1 - 2 * guodugrid2) + hou1

        # 生成角度列表
        thetaall = []
        for j in range(len(neix)):
            if neix[j] < 0:
                k1 = (neiy[j + 1] - neiy[j]) / (neix[j + 1] - neix[j])
                theta1 = arctan(k1) + pi / 2
                thetaall.append(theta1)
            if 0 <= neix[j] <= tschangdu:
                thetaall.append(90)
            if neix[j] > tschangdu:
                k1 = (neiy[j - 1] - neiy[j]) / (neix[j - 1] - neix[j])
                theta1 = arctan(k1) + pi / 2
                thetaall.append(theta1)

        # 新建环向层
        newx = []
        newy = []
        for j in range(len(neix)):
            if neix[j] < 0:
                newx.append(neix[j] + cos(thetaall[j]) * houall[j])
                newy.append(neiy[j] + sin(thetaall[j]) * houall[j])
            if 0 <= neix[j] <= tschangdu:
                newx.append(neix[j])
                newy.append(neiy[j] + houall[j])
            if neix[j] > tschangdu:
                newx.append(neix[j] + cos(thetaall[j]) * houall[j])
                newy.append(neiy[j] + sin(thetaall[j]) * houall[j])
        huan_nx.append(neix)
        huan_ny.append(neiy)
        huan_wx.append(newx)
        huan_wy.append(newy)

        # 更新上层厚度
        for j in range(ind3, len(lunkuoneix)):
            leflen = lunkuoneix[j].index(zhongmaxx) - neix.index(zhongmaxx)
            riglen = len(lunkuoneix[j]) - len(neix) - leflen
            houall1 = [0] * leflen + houall + [0] * riglen  # 对轮廓整体偏移
            thetaall1 = [0] * leflen + thetaall + [0] * riglen

            newnx = []
            newny = []
            newwx = []
            newwy = []
            for m in range(len(lunkuoneix[j])):
                if lunkuoneix[j][m] < 0:
                    newnx.append(lunkuoneix[j][m] + cos(thetaall1[m]) * houall1[m])
                    newny.append(lunkuoneiy[j][m] + sin(thetaall1[m]) * houall1[m])
                    newwx.append(lunkuowaix[j][m] + cos(thetaall1[m]) * houall1[m])
                    newwy.append(lunkuowaiy[j][m] + sin(thetaall1[m]) * houall1[m])
                if 0 <= lunkuoneix[j][m] <= tschangdu:
                    newnx.append(lunkuoneix[j][m])
                    newny.append(lunkuoneiy[j][m] + houall1[m])
                    newwx.append(lunkuowaix[j][m])
                    newwy.append(lunkuowaiy[j][m] + houall1[m])
                if lunkuoneix[j][m] > tschangdu:
                    newnx.append(lunkuoneix[j][m] + cos(thetaall1[m]) * houall1[m])
                    newny.append(lunkuoneiy[j][m] + sin(thetaall1[m]) * houall1[m])
                    newwx.append(lunkuowaix[j][m] + cos(thetaall1[m]) * houall1[m])
                    newwy.append(lunkuowaiy[j][m] + sin(thetaall1[m]) * houall1[m])
            lunkuoneix[j] = newnx
            lunkuoneiy[j] = newny
            lunkuowaix[j] = newwx
            lunkuowaiy[j] = newwy

    else:  # 补强
        pass

# ---------------------------------------------------------------------------------------------
# 五、添加补强，更新左右轮廓数据点
'''
补强层单独建立数据点列表储存，同时更新螺旋缠绕（LAM）数据点
'''
buqiangzuo_nx = []
buqiangzuo_ny = []
buqiangzuo_wx = []
buqiangzuo_wy = []

buqiangyou_nx = []
buqiangyou_ny = []
buqiangyou_wx = []
buqiangyou_wy = []

guodugrid3 += 1
for i in range(len(buqiangtable)):
    if buqiangtable[i][3] == 90 and buqiangtable[i][1] <= (tschangdu / 2) <= buqiangtable[i][2]:
        pass
    elif buqiangtable[i][2] < 0:  # 左侧补强
        ind4 = buqiangtable[i][0]
        hou = buqiangtable[i][4]
        bzs = 0
        bys = 0
        bys1 = 0
        # 生成内轮廓
        for j in range(len(BQNzuoX[ind4])):
            if BQNzuoX[ind4][j] <= buqiangtable[i][1] < BQNzuoX[ind4][j + 1]:
                bzs = j
            if BQNzuoX[ind4][j - 1] < buqiangtable[i][2] <= BQNzuoX[ind4][j]:
                bys1 = j - len(BQNzuoX[ind4])  # 倒索引 更新上层轮廓时方便定位
                bys = j  # 正索引
        neix = BQNzuoX[ind4][bzs:bys + 1]
        neiy = BQNzuoY[ind4][bzs:bys + 1]

        # 生成厚度列表
        # houall = [0] + [hou] * (bys - bzs + 1 - 2) + [0]
        hou0 = list(linspace(0, hou, guodugrid3))
        hou1 = list(linspace(hou, 0, guodugrid3))
        houall = hou0 + [hou] * (bys - bzs + 1 - 2 * guodugrid3) + hou1

        # 生成角度列表（第一个点处厚度为0，角度不影响，设为0）
        thetaall = [0]
        for j in range(1, len(neix)):
            k1 = (neiy[j] - neiy[j - 1]) / (neix[j] - neix[j - 1])
            theta1 = arctan(k1) + pi / 2
            thetaall.append(theta1)
        # 新建补强层
        newx = [neix[0]]
        newy = [neiy[0]]
        for j in range(1, len(neix)):
            newx.append(neix[j] + cos(thetaall[j]) * houall[j])
            newy.append(neiy[j] + sin(thetaall[j]) * houall[j])
        buqiangzuo_nx.append(neix)
        buqiangzuo_ny.append(neiy)
        buqiangzuo_wx.append(newx)
        buqiangzuo_wy.append(newy)

        # 更新上层轮廓
        for j in range(ind4, len(lunkuoneix)):
            r0 = lunkuoneix[j].index(0) + bys1 + 1
            riglen = len(lunkuoneix[j][r0 + 1:])
            if riglen + len(houall) < len(lunkuoneix[j]):
                leflen = len(lunkuoneix[j]) - len(houall) - riglen
                houall1 = [0] * leflen + houall + [0] * riglen  # 对整个轮廓（lunkuoneix、、、）整体偏移
                thetaall1 = [0] * leflen + thetaall + [0] * riglen
            else:
                leflen = -(len(lunkuoneix[j]) - len(houall) - riglen)
                houall1 = houall[leflen:] + [0] * riglen
                thetaall1 = thetaall[leflen:] + [0] * riglen

            newnx = []
            newny = []
            newwx = []
            newwy = []
            for m in range(len(lunkuoneix[j])):
                if lunkuoneix[j][m] <= 0:
                    newnx.append(lunkuoneix[j][m] + cos(thetaall1[m]) * houall1[m])
                    newny.append(lunkuoneiy[j][m] + sin(thetaall1[m]) * houall1[m])
                    newwx.append(lunkuowaix[j][m] + cos(thetaall1[m]) * houall1[m])
                    newwy.append(lunkuowaiy[j][m] + sin(thetaall1[m]) * houall1[m])
                else:
                    newnx.append(lunkuoneix[j][m])
                    newny.append(lunkuoneiy[j][m])
                    newwx.append(lunkuowaix[j][m])
                    newwy.append(lunkuowaiy[j][m])

            lunkuoneix[j] = newnx
            lunkuoneiy[j] = newny
            lunkuowaix[j] = newwx
            lunkuowaiy[j] = newwy

        # 更新上层补强用内轮廓BQNzuox
        for j in range(ind4, len(BQNzuoX)):
            riglen = -bys1 - 1
            leflen = len(BQNzuoX[j]) - len(houall) - riglen
            houall1 = [0] * leflen + houall + [0] * riglen
            thetaall1 = [0] * leflen + thetaall + [0] * riglen
            newnx = []
            newny = []
            for m in range(len(BQNzuoX[j])):
                newnx.append(BQNzuoX[j][m] + cos(thetaall1[m]) * houall1[m])
                newny.append(BQNzuoY[j][m] + sin(thetaall1[m]) * houall1[m])

            BQNzuoX[j] = newnx
            BQNzuoY[j] = newny

    elif buqiangtable[i][1] > tschangdu:  # 右侧补强
        ind4 = buqiangtable[i][0]
        hou = buqiangtable[i][4]
        bzs = 0
        bys = 0
        bys1 = 0
        # 生成内轮廓
        for j in range(len(BQNyouX[ind4])):
            if BQNyouX[ind4][j] <= buqiangtable[i][1] < BQNyouX[ind4][j + 1]:
                bzs = j
            if BQNyouX[ind4][j - 1] < buqiangtable[i][2] <= BQNyouX[ind4][j]:
                bys1 = j - len(BQNyouX[ind4])  # 倒索引 更新上层轮廓时方便定位
                bys = j  # 正索引
        neix = BQNyouX[ind4][bzs:bys + 1]
        neiy = BQNyouY[ind4][bzs:bys + 1]

        # 生成厚度列表
        # houall = [0] + [hou] * (bys - bzs + 1 - 2) + [0]
        hou0 = list(linspace(0, hou, guodugrid3))
        hou1 = list(linspace(hou, 0, guodugrid3))
        houall = hou0 + [hou] * (bys - bzs + 1 - 2 * guodugrid3) + hou1

        # 生成角度列表（第一个点处厚度为0，角度不影响，设为0）
        thetaall = [0]
        for j in range(1, len(neix)):
            k1 = (neiy[j] - neiy[j - 1]) / (neix[j] - neix[j - 1])
            theta1 = arctan(k1) + pi / 2
            thetaall.append(theta1)
        # 新建补强层
        newx = [neix[0]]
        newy = [neiy[0]]
        for j in range(1, len(neix)):
            newx.append(neix[j] + cos(thetaall[j]) * houall[j])
            newy.append(neiy[j] + sin(thetaall[j]) * houall[j])
        buqiangyou_nx.append(neix)
        buqiangyou_ny.append(neiy)
        buqiangyou_wx.append(newx)
        buqiangyou_wy.append(newy)

        # 更新上层轮廓
        for j in range(ind4, len(lunkuoneix)):
            l0 = lunkuoneix[j].index(tschangdu) + bzs
            leflen = len(lunkuoneix[j][:l0])
            houall1 = [0] * leflen + houall + [0] * n02
            thetaall1 = [0] * leflen + thetaall + [0] * n02
            newnx = []
            newny = []
            newwx = []
            newwy = []
            for m in range(len(lunkuoneix[j])):
                if lunkuoneix[j][m] >= tschangdu:
                    newnx.append(lunkuoneix[j][m] + cos(thetaall1[m]) * houall1[m])
                    newny.append(lunkuoneiy[j][m] + sin(thetaall1[m]) * houall1[m])
                    newwx.append(lunkuowaix[j][m] + cos(thetaall1[m]) * houall1[m])
                    newwy.append(lunkuowaiy[j][m] + sin(thetaall1[m]) * houall1[m])
                else:
                    newnx.append(lunkuoneix[j][m])
                    newny.append(lunkuoneiy[j][m])
                    newwx.append(lunkuowaix[j][m])
                    newwy.append(lunkuowaiy[j][m])

            lunkuoneix[j] = newnx
            lunkuoneiy[j] = newny
            lunkuowaix[j] = newwx
            lunkuowaiy[j] = newwy

        # 更新上层补强用内轮廓BQNyoux
        for j in range(ind4, len(BQNyouX)):
            leflen = bzs
            riglen = len(BQNyouX[j]) - len(houall) - leflen
            houall1 = [0] * leflen + houall + [0] * riglen
            thetaall1 = [0] * leflen + thetaall + [0] * riglen
            newnx = []
            newny = []
            for m in range(len(BQNyouX[j])):
                newnx.append(BQNyouX[j][m] + cos(thetaall1[m]) * houall1[m])
                newny.append(BQNyouY[j][m] + sin(thetaall1[m]) * houall1[m])

            BQNyouX[j] = newnx
            BQNyouY[j] = newny

# 六、abaqus前处理
'''
lunkuoneix,lunkuoneiy   lunkuowaix,lunkuowaiy
huan_nx,huan_ny   huan_wx,huan_wy
buqiangzuo_nx,buqiangzuo_ny   buqiangzuo_wx,buqiangzuo_wy
buqiangyou_nx,buqiangyou_ny   buqiangyou_wx,buqiangyou_wy
angle
h_angle
bq_angle
'''
# 所有数据保留三位小数
if 1:
    for j in range(len(lunkuoneix)):
        lunkuoneix[j] = [round(i, 3) for i in lunkuoneix[j]]
        lunkuoneiy[j] = [round(i, 3) for i in lunkuoneiy[j]]
        lunkuowaix[j] = [round(i, 3) for i in lunkuowaix[j]]
        lunkuowaiy[j] = [round(i, 3) for i in lunkuowaiy[j]]
    for j in range(len(huan_nx)):
        huan_nx[j] = [round(i, 3) for i in huan_nx[j]]
        huan_ny[j] = [round(i, 3) for i in huan_ny[j]]
        huan_wx[j] = [round(i, 3) for i in huan_wx[j]]
        huan_wy[j] = [round(i, 3) for i in huan_wy[j]]
    for j in range(len(buqiangzuo_nx)):
        buqiangzuo_nx[j] = [round(i, 3) for i in buqiangzuo_nx[j]]
        buqiangzuo_ny[j] = [round(i, 3) for i in buqiangzuo_ny[j]]
        buqiangzuo_wx[j] = [round(i, 3) for i in buqiangzuo_wx[j]]
        buqiangzuo_wy[j] = [round(i, 3) for i in buqiangzuo_wy[j]]
    for j in range(len(buqiangyou_nx)):
        buqiangyou_nx[j] = [round(i, 3) for i in buqiangyou_nx[j]]
        buqiangyou_ny[j] = [round(i, 3) for i in buqiangyou_ny[j]]
        buqiangyou_wx[j] = [round(i, 3) for i in buqiangyou_wx[j]]
        buqiangyou_wy[j] = [round(i, 3) for i in buqiangyou_wy[j]]

# 整理角度数据，全轮廓建模、环向建模、补强建模
for i in range(len(LAMx)):
    plt.plot(LAMx[i], LAMy[i], 'k>-', linewidth=len(LAMx))

for ji in range(len(lunkuoneix)):
    # if ji % 2:
    #     plt.plot(lunkuoneix[ji], lunkuoneiy[ji], 'o-', linewidth=len(lunkuoneix) - ji)
    #     plt.plot(lunkuowaix[ji], lunkuowaiy[ji], 'o-', linewidth=len(lunkuoneix) - ji)
    # else:
    plt.plot(lunkuoneix[ji], lunkuoneiy[ji], '*-', linewidth=len(lunkuoneix) - ji)
    plt.plot(lunkuowaix[ji], lunkuowaiy[ji], '*-', linewidth=len(lunkuoneix) - ji)

# for ji in range(len(huan_nx)):
#     plt.plot(huan_nx[ji], huan_ny[ji], 'o-')
#     plt.plot(huan_wx[ji], huan_wy[ji], 'o-')
#
# for ji in range(len(buqiangzuo_nx)):
#     plt.plot(buqiangzuo_nx[ji], buqiangzuo_ny[ji], 'o-')
#     plt.plot(buqiangzuo_wx[ji], buqiangzuo_wy[ji], 'o-')
#
# for ji in range(len(buqiangyou_nx)):
#     plt.plot(buqiangyou_nx[ji], buqiangyou_ny[ji], 'o-')
#     plt.plot(buqiangyou_wx[ji], buqiangyou_wy[ji], 'o-')
plt.axis("equal")
plt.show()
