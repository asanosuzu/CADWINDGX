#!/usr/bin/env python
# -*- coding:utf-8 -*-
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
from math import *
from numpy import *
import numpy as np
import os
from math import *
import numpy as nmp

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)
def yitihuaChaiFen(data):
    a = data
    Line = zeros((1, 4))
    Aa = zeros((len(a), 4))
    for i in range(len(a)):  # ѭ����ֵ
        Line0 = a[i].split()
        Aa[i][0] = float(Line0[0])
        Aa[i][1] = float(Line0[1])/2#���ļ��е�ֱ��ֵת��Ϊ�뾶ֵ
        Aa[i][2] = float(Line0[2])
        Aa[i][3] = float(Line0[3])
    Aa = Aa[Aa[:, 0].argsort()]  # ���յ�1�ж�������
       # Rmax = max(Aa[0:, 1])  # ��ȡ���ֵ
    # tmin = min(Aa[0:, 3])  # ��ȡ��Сֵ
    # c = np.where(Aa == max(Aa[0:, 1]))  # ��ȡֱ�����ֵ�����кź��кţ�����Ͳ��ε�ֱ��ֵ
    # return [Aa,c,Rmax,tmin]
    return [Aa]
def yitihuaDataSolve(data):
    chaifen0=yitihuaChaiFen(data)#��ֳ�����ֵ
    Aa=chaifen0[0]

#Ԥ����
    # ����������
    X =[]
    R =[]
    alpha =[]
    h = []
    # �ǶȺͺ����
    X11 = []
    R11 = []
    alpha11 = []
    h11 = []

#ѭ����ֵ
    for i1 in range(len(Aa)):
        # ������
        X.append(Aa[i1][0]);
        R.append(Aa[i1][1]);#�뾶ֵ���ļ�������ֱ��ֵ�����ڲ�ֺ�������ת��Ϊ�뾶
        # alpha.append(Aa[i1][2]);
        # h.append(Aa[i1][3]);

        # ���ǶȺͺ��
        # if Aa[i1][2]>0:#ֻ��ȡһ��ѭ��������
        #     X11.append(Aa[i1][0]);
        #     R11.append(Aa[i1][1]);  # �뾶ֵ���ļ�������ֱ��ֵ�����ڲ�ֺ�������ת��Ϊ�뾶
        #     alpha11.append(Aa[i1][2]);
        #     h11.append(Aa[i1][3]);

        # ���ȫ�����
        X11.append(Aa[i1][0]);
        R11.append(Aa[i1][1]);  # �뾶ֵ���ļ�������ֱ��ֵ�����ڲ�ֺ�������ת��Ϊ�뾶
        alpha11.append(Aa[i1][2]);
        h11.append(Aa[i1][3]);

# ��ȡ�ظ�ֵ�к�
    hanghao= []
    for ii1 in range(len(Aa) - 1):
        if Aa[ii1 + 1][0] == Aa[ii1][0] and abs(Aa[ii1 + 1][2]) == abs(Aa[ii1][2]):  # λͬ��ͬ(ȡ����ֵ)
            hanghao.append(ii1)
        else:
            pass
        if Aa[ii1 + 1][0] == Aa[ii1][0] and abs(Aa[ii1 + 1][2]) != abs(Aa[ii1][2]):  # λͬ�ǲ�ͬ(ȡ����ֵ)
            hanghao.append(ii1)
        else:
            pass

    hanghao1 = []
    for ii1 in range(len(X11) - 1):
        if X11[ii1 + 1] == X11[ii1] and abs(alpha11[ii1 + 1]) == abs(alpha11[ii1]):  # λͬ��ͬ(ȡ����ֵ)
            hanghao1.append(ii1)
        else:
            pass
        if X11[ii1 + 1] == X11[ii1] and abs(alpha11[ii1 + 1]) != abs(alpha11[ii1]):  # λͬ�ǲ�ͬ(ȡ����ֵ)
            hanghao1.append(ii1)
        else:
            pass

# ȥ���ظ�����ֵ
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

# 2020.8.23�ģ����ܳ����޶������β���½���
#     weizhi=[i for i in range(len(X)) if X[i]>(changdu-fengtoucha) and (R[i]-R[i-1])<0]
#     X=X[0:weizhi[0]]
#     R=R[0:weizhi[0]]


    weizhi=np.where(X11<=max(X))
    # weizhi=max([i for i in range(len(X11)) if X11[i]<=X[weizhi[-1]]])
    X11 = X11[0:weizhi[0][-1]+1]
    R11 = R11[0:weizhi[0][-1]+1]
    alpha11 = alpha11[0:weizhi[0][-1]+ 1]
    h11 = h11[0:weizhi[0][-1] + 1]

    return [X,R,X11,R11,alpha11,h11]###X11,alpha11ԭʼLAM�ļ�λ�ýǶ�

###########################################################################
# Class definition
###########################################################################

xyplotname=0
class Yitihua2DB(AFXDataDialog):
    [ID_SAVE ,ID_INPUT,ID_CAOTUHUIZHI]= range(AFXForm.ID_LAST, AFXForm.ID_LAST+3)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):
        self.form = form
        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, '��ά���Ƹ��ϲ��ϻ������������CADWindתabaqus���ٽ�ģ���',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        VFrame_1 = FXVerticalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
            
        GroupBox_1 = FXGroupBox(p=VFrame_1, text='�ļ�ָ��', opts=FRAME_GROOVE)    
            
        fileHandler = Yitihua2DBFileHandler(form, 'fileName', '(*.LAM)')
        fileTextHf = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        self.filename=AFXTextField(p=fileTextHf, ncols=20, labelText='ָ��CadWind lam��ʽ���ļ�', tgt=form.fileNameKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
        FXButton(p=GroupBox_1, text='��ͼԤ��', ic=None, tgt=self, sel=self.ID_CAOTUHUIZHI)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CAOTUHUIZHI, Yitihua2DB.caotuhuizhi)
        
        GroupBox_2 = FXGroupBox(p=VFrame_1, text='���Ʋ���ָ��', opts=FRAME_GROOVE)
        VAligner_1 = AFXVerticalAligner(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
        self.pressure = AFXTextField(p=VAligner_1, ncols=12, labelText='��Ʊ�ѹ/MPa', tgt=form.pressureKw, sel=0)
        self.hxdt = AFXTextField(p=VAligner_1, ncols=12, labelText='Ͳ���򵥲���/mm', tgt=form.hxdtKw, sel=0)
        # AFXTextField(p=VAligner_1, ncols=12, labelText='Ͳ������������/mm', tgt=form.lxdtKw, sel=0)
        self.zhuanjiao = AFXTextField(p=VAligner_1, ncols=12, labelText='��άģ����ת�Ƕ�/��', tgt=form.zhuanjiaoKw, sel=0)
        # AFXTextField(p=VAligner_1, ncols=12, labelText='Ͳ���������ƽǶ�/��', tgt=form.luoxuanjiaoKw, sel=0)
        
        GroupBox_3 = FXGroupBox(p=VFrame_1, text='��Ʋ���ָ��', opts=FRAME_GROOVE|LAYOUT_FILL_X|LAYOUT_FILL_Y)
        
        TabBook_1 = FXTabBook(p=GroupBox_3, tgt=None, sel=0,
            opts=TABBOOK_NORMAL,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='������������', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        VFrame_1 = FXVerticalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0) 

        fileName = os.path.join(thisDir, 'pic2.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=VFrame_1, text='', ic=icon)
        
        VAligner_2 = AFXVerticalAligner(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        ##########    
        # AFXTextField(p=VAligner_2, ncols=12, labelText='��ͷ���װ뾶/mm(a)', tgt=form.R0_jikongKw, sel=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='β��ڰ뾶/mm(b)', tgt=form.R0_weipenguanKw, sel=0)
        self.changdu = AFXTextField(p=VAligner_2, ncols=12, labelText='���׵�β����ܳ���/mm(c)', tgt=form.changduKw, sel=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='����Բ����ͷ���׾���/mm(d)', tgt=form.fengtouchaKw, sel=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='�ҳ��Բ�����󲿾���/mm(e)', tgt=form.youfengtouKw, sel=0)
        self.tschangdu = AFXTextField(p=VAligner_2, ncols=12, labelText='Ͳ����/mm(f)', tgt=form.tschangduKw, sel=0)
        self.jinshunei = AFXTextField(p=VAligner_2, ncols=12, labelText='�ҳ��Բ��������ͷ����/mm(g)', tgt=form.jinshuneiKw, sel=0)
        ##########
        tabItem = FXTabItem(p=TabBook_1, text='���̳�������', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_2 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
            
        VAligner_3 = AFXVerticalAligner(p=TabItem_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)#���벼��
        
        ################################
            
        self.E1 = AFXTextField(p=VAligner_3, ncols=12, labelText='E1', tgt=form.E1Kw, sel=0)
        self.E2 = AFXTextField(p=VAligner_3, ncols=12, labelText='E2', tgt=form.E2Kw, sel=0)
        self.E3 = AFXTextField(p=VAligner_3, ncols=12, labelText='E3', tgt=form.E3Kw, sel=0)
        self.Nu12 = AFXTextField(p=VAligner_3, ncols=12, labelText='Nu12', tgt=form.Nu12Kw, sel=0)
        self.Nu13 = AFXTextField(p=VAligner_3, ncols=12, labelText='Nu13', tgt=form.Nu13Kw, sel=0)
        self.Nu23 = AFXTextField(p=VAligner_3, ncols=12, labelText='Nu23', tgt=form.Nu23Kw, sel=0)
        self.G12 = AFXTextField(p=VAligner_3, ncols=12, labelText='G12', tgt=form.G12Kw, sel=0)
        self.G13 = AFXTextField(p=VAligner_3, ncols=12, labelText='G13', tgt=form.G13Kw, sel=0)
        self.G23 = AFXTextField(p=VAligner_3, ncols=12, labelText='G23', tgt=form.G23Kw, sel=0)
        #####################################
        tabItem = FXTabItem(p=TabBook_1, text='����˳������', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_3 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vf = FXVerticalFrame(TabItem_3, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        self.table = AFXTable(vf, 15, 2, 11, 2, form.pucengKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.table.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE|AFXTable.POPUP_WRITE_TO_FILE)
        self.table.setLeadingRows(1)
        self.table.setLeadingColumns(1)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnType(1, AFXTable.TEXT)
        #table.setColumnWidth(2, 100)
        #table.setColumnType(2, AFXTable.TEXT)
        self.table.setLeadingRowLabels('��������ѭ��(һ��ѭ������)   ������Ƶ���\t')
        self.table.setStretchableColumn( self.table.getNumColumns()-1 )
        #����������ѡ��
        self.table.setColumnJustify(1,AFXTable.CENTER)
        listId1 = self.table.addList('HelixLoop\tHoop\t')
        self.table.setColumnType(1,AFXTable.LIST)
        self.table.setColumnListId(1,listId1)        
        
        self.table.showHorizontalGrid(True)
        self.table.showVerticalGrid(True)
        
        
        GroupBox_111 = FXGroupBox(p=self, text='���ݴ���', opts=FRAME_GROOVE)
        HFrame_10 = FXHorizontalFrame(p=GroupBox_111, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
            


        FXButton(p=HFrame_10, text='����', ic=None, tgt=self, sel=self.ID_SAVE) 
        FXButton(p=HFrame_10, text='����', ic=None, tgt=self, sel=self.ID_INPUT)            


        FXMAPFUNC(self, SEL_COMMAND, self.ID_SAVE, Yitihua2DB.saveToDatabase)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_INPUT, Yitihua2DB.DatabaseToGui)
        
        
        fileHandler = FileDBFileHandler(form, 'dataBaseName', '(*.par3)')
        fileTextHf = FXHorizontalFrame(p=HFrame_10, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        self.files = AFXTextField(p=fileTextHf, ncols=12, labelText='   �ļ���:', tgt=form.dataBaseNameKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        self.files.disable()
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)


    def countTable(self):
        datafilename=self.form.dataBaseNameKw.getValue()
        countTable1,countTable2 = 1,1
        column = 2
        f=file(datafilename,'r')
        for each_line in f:
            data=each_line.strip().split(',')
            if data[0] == "P1_AFXTable1":
                countTable1+=1
        if countTable1 == 1:
            countTable1+=1
        self.table.setTableSize(countTable1,column)

        


    def DatabaseToGui(self, sender, sel, ptr):
    #����Ĭ�ϲ������ݿ��ļ�
        datafilename=self.form.dataBaseNameKw.getValue()
        self.countTable()
        f=file(datafilename,'r')
        k=1
        j=1 

        while True:
            line=f.readline()          
            if len(line)==0:
                break
            data=line.strip().split(',')
            if data[0] == "P1_AFXTextField":
            
                if data[1] == "pressure":
                    self.form.pressureKw.setValue(data[2])
                elif data[1] == "zhuanjiao":
                    self.form.zhuanjiaoKw.setValue(data[2])
                elif data[1] == "changdu":
                    self.form.changduKw.setValue(data[2])
                elif data[1] == "tschangdu":
                    self.form.tschangduKw.setValue(data[2])
                elif data[1] == "jinshunei":
                    self.form.jinshuneiKw.setValue(data[2])
                elif data[1] == "E1":
                    self.form.E1Kw.setValue(data[2])
                elif data[1] == "E2":
                    self.form.E2Kw.setValue(data[2])
                elif data[1] == "E3":
                    self.form.E3Kw.setValue(data[2])
                elif data[1] == "Nu12":
                    self.form.Nu12Kw.setValue(data[2])
                elif data[1] == "Nu13":
                    self.form.Nu13Kw.setValue(data[2])
                elif data[1] == "Nu23":
                    self.form.Nu23Kw.setValue(data[2])
                    
                elif data[1] == "G12":
                    self.form.G12Kw.setValue(data[2])
                elif data[1] == "G13":
                    self.form.G13Kw.setValue(data[2])
                elif data[1] == "G23":
                    self.form.G23Kw.setValue(data[2])                                        
                else:
                    pass
            elif data[0] == "P1_AFXTable1":
                self.table.setItemText(k,1, data[1])
                k+=1

        self.form.dataBaseNameKw.setValue("")           
        mw = getAFXApp().getAFXMainWindow()
        mw.writeToMessageArea("Parameters imported successfully")
        
    
    def caotuhuizhi(self, sender, sel, ptr):
        
        global xyplotname
        if SELID(sel) == self.ID_CAOTUHUIZHI:
            
            Lam1 = open(self.filename.getText(),'r')#fileName D:\\temp\\test\\444.LAM'
            data1 = Lam1.readlines()
            Lam1.close()
            del (data1[0:2])  # ɾ��ǰ������з���ֵ��,CadwindĬ�����ɵķ�������

            # ��ʼ�����ݴ洢����
            # �˵�ֵ
            # ��
            XddianZ=[]
            RddianZ=[]
            # ��
            XddianY=[]
            RddianY=[]

            # ����
            # �ڱ���
            neisX=[]
            neisR=[]
            # �����
            waisX=[]
            waisR=[]

            ######################################################################################################################


            # �õ����봦���ĳ�������
            #�ڱ���
            # �õ����ڲ���������������ƵĽǶ�����
            # �õ���������ֵ
            # data=yitihuaDataSolve(data1,changdu,fengtouchazuo)
            data=yitihuaDataSolve(data1)
            #����������
            X1=data[0]
            R1=data[1]
            # �Ƕȸ�����
            X12=data[2]
            R12=data[3]
            alpha1=data[4]
            h1=data[5]

            xydata=zip(X1,R1)
            xydata=session.XYData(data=xydata,name='xydata',legendLabel='lunkuoyulan',xValuesLabel='X',yValuesLabel='Y')
            #====================generate the curve to plot==========================#
            xyCurve=session.Curve(xyData=xydata)
            xyCurve.setValues(displayTypes=(LINE,),legendLabel='lunkuoCurve',useDefault=OFF)
            # xyCurve.lineStyle.setValues(style=SOLID,thickness=1.0,color='Black')
            # xyCurve.symbolStyle.setValues(show=OFF)
            #====================generate picture=========================#
            # scPlot=session.XYPlot(name='lunkuoyulan')
            # scPlot.title.setValues(text='lunkuoyulan')
            # chartName=scPlot.charts.keys()[0]
            # chart=scPlot.charts[chartName]
            # chart.setValues(curvesToPlot=(xyCurve,),)
            # chart.gridArea.style.setValues(color='White')
            # myViewport=session.Viewport(name='myViewport',border=OFF,titleBar=OFF,titleStyle=CUSTOM,customTitleString='Viewport Example of XYPlot')
            # myViewport.setValues(width=120,height=80,origin=(0,0))
            # myViewport.setValues(displayedObject=scPlot)

            session.viewports['Viewport: 1'].setValues(displayedObject=None)
            xyp = session.XYPlot(name='XYPlot'+str(xyplotname))
            chartName = xyp.charts.keys()[0]
            chart = xyp.charts[chartName]
            xy1 = session.xyDataObjects['xydata']
            c1 = session.Curve(xyData=xy1)
            chart.setValues(curvesToPlot=(c1, ), )
            session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
            xyplotname+=1
            
        

    def saveToDatabase(self, sender, sel, ptr):
        if SELID(sel) == self.ID_SAVE:
            datafilename=self.form.dataBaseNameKw.getValue()
            if datafilename[-5:] !=".par3":
                datafilename+=".par3"
            #thisPath = os.path.abspath(__file__)                                                      
            #thisDir = os.path.dirname(thisPath)                                                              
            #filename= os.path.join(thisDir, 'config_database.dat') 
            f = open(datafilename,'w')
            
            #####################textfield���ݱ���######################
            pressurehValue = self.pressure.getText()
            zhuanjiaoValue = self.zhuanjiao.getText()
            changduValue = self.changdu.getText()
            tschangduValue = self.tschangdu.getText()
            jinshuneiValue = self.jinshunei.getText()
            E1Value = self.E1.getText()
            E2Value = self.E2.getText()
            E3Value = self.E3.getText()
            Nu12Value = self.Nu12.getText()
            Nu13Value = self.Nu13.getText()
            Nu23Value = self.Nu23.getText()
            G12Value = self.G12.getText()
            G13Value = self.G13.getText()
            G23Value = self.G23.getText()

            
        
            f.writelines("P1_AFXTextField,pressure,%s\n"%pressurehValue)  
            f.writelines("P1_AFXTextField,zhuanjiao,%s\n"%zhuanjiaoValue)
            f.writelines("P1_AFXTextField,changdu,%s\n"%changduValue)  
            f.writelines("P1_AFXTextField,tschangdu,%s\n"%tschangduValue)  
            f.writelines("P1_AFXTextField,jinshunei,%s\n"%jinshuneiValue)  
            f.writelines("P1_AFXTextField,E1,%s\n"%E1Value)  
            f.writelines("P1_AFXTextField,E2,%s\n"%E2Value)  
            f.writelines("P1_AFXTextField,E3,%s\n"%E3Value)              
            f.writelines("P1_AFXTextField,Nu12,%s\n"%Nu12Value)  
            f.writelines("P1_AFXTextField,Nu13,%s\n"%Nu13Value)
            f.writelines("P1_AFXTextField,Nu23,%s\n"%Nu23Value)
            
            f.writelines("P1_AFXTextField,G12,%s\n"%G12Value)
            f.writelines("P1_AFXTextField,G13,%s\n"%G13Value)
            f.writelines("P1_AFXTextField,G23,%s\n"%G23Value)
            

###################������ݱ���###########
            #####���1########
            rowNums1=self.table.getNumRows()   

            for i in range(1,rowNums1):
                column1=self.table.getItemValue(i,1)
                f.writelines("P1_AFXTable1,%s\n"%column1)
                
            f.close()
            self.form.dataBaseNameKw.setValue("")   
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea("save all data to dataBase!\npath:%s\n"%datafilename)        
###########################################################################
# Class definition
###########################################################################

class Yitihua2DBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, Yitihua2DBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.fileNameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.odb')
       fileDb.create()
       fileDb.showModal()



class FileDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, FileDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'save a File',
           self.fileNameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.odb')
       fileDb.create()
       fileDb.showModal()