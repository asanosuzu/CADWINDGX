#!/usr/bin/python
#-*-coding: UTF-8-*-
#-*-coding: mbcs -*- 
from abaqusConstants import *

from abaqusGui import *
from kernelAccess import mdb, session
import os
# from help_aa_form import Help_aa_form

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class Wind3DB(AFXDataDialog):
    [ID_CHECK,ID_SAVE ,ID_INPUT,ID_COPYTABLE,ID_LEFTPASTEABLE,ID_RIGHTPASTEABLE]= range(AFXForm.ID_LAST, AFXForm.ID_LAST+6)

    
    # ID_HELP = AFXForm.ID_LAST+2
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):
        self.form = form
        self.layupData = []
        # Construct the base class.
        #
        # self.Help_aa_form = Help_aa_form(form.getOwner())
        AFXDataDialog.__init__(self, form, '复合材料压力容器建模插件',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        self.form=form    

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')

        GroupBox_1 = FXGroupBox(p=self, text='参数化建模', opts=FRAME_GROOVE)
        VFrame_1 = FXVerticalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        HFrame_1 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
       
        GroupBox_3 = FXGroupBox(p=HFrame_1, text='建模参数', opts=FRAME_GROOVE)
        VAligner_2 = AFXVerticalAligner(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        self.L_segmentationNum = AFXTextField(p=VAligner_2, ncols=12, labelText='左封头切片数:', tgt=form.L_segmentationNumKw, sel=0)
        self.R_segmentationNum = AFXTextField(p=VAligner_2, ncols=12, labelText='右封头切片数:', tgt=form.R_segmentationNumKw, sel=0)
        self.rotationAngle = AFXTextField(p=VAligner_2, ncols=12, labelText='模型旋转角:', tgt=form.rotationAngleKw, sel=0)
        
        VFrame_2 = FXVerticalFrame(p=HFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
        HFrame_21 = FXHorizontalFrame(p=VFrame_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        HFrame_22 = FXHorizontalFrame(p=VFrame_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
        self.computing_method=AFXComboBox(p=HFrame_22, ncols=0, nvis=1, text='计算方法:', tgt=form.computing_methodKw, sel=0)
        FXLabel(p=HFrame_22, text='       ', ic=None)
        self.material_property=AFXComboBox(p=HFrame_22, ncols=0, nvis=1, text='材料赋属性方法:', tgt=form.material_propertyKw, sel=0)
        
        self.computing_method.appendItem('Cubic-spline')
        self.computing_method.appendItem('B-spline')
        self.material_property.appendItem('Assign section')
        self.material_property.appendItem('create composite layup')
        
        GroupBox_6 = FXGroupBox(p=HFrame_21, text='其他参数', opts=FRAME_GROOVE)
        VAligner_3 = AFXVerticalAligner(p=GroupBox_6, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        #self.fibersWidth = AFXTextField(p=VAligner_3, ncols=12, labelText='纱线宽度:', tgt=form.fibersWidthKw, sel=0)
        self.pieceNumber = AFXTextField(p=VAligner_3, ncols=12, labelText='网格轴向分片:', tgt=form.pieceNumberKw, sel=0)
        self.approximateSize = AFXTextField(p=VAligner_3, ncols=12, labelText='网格近似尺寸:', tgt=form.approximateSizeKw, sel=0)

        
        HFrame_111 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,pl=0, pr=0, pt=0, pb=0)
        
        VFrame_21 = FXVerticalFrame(p=HFrame_111, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)    
    
        # HFrame_2 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            # pl=0, pr=0, pt=0, pb=0)
        GroupBox_4 = FXGroupBox(p=VFrame_21, text='缠绕层建模参数', opts=FRAME_GROOVE)
        vf = FXVerticalFrame(GroupBox_4, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        
      
        #self.num=k #定义表格的总行数        
        self.table = AFXTable(vf, 13, 13, 13, 13, form.L_styleKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.table.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE|AFXTable.POPUP_WRITE_TO_FILE)
        self.table.setLeadingRows(1)
        self.table.setLeadingColumns(1)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnType(1, AFXTable.LIST)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnType(2, AFXTable.FLOAT)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnType(3, AFXTable.LIST)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnType(4, AFXTable.FLOAT)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnType(5, AFXTable.FLOAT)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnType(6, AFXTable.FLOAT)
        self.table.setColumnWidth(7, 80)
        self.table.setColumnType(7, AFXTable.FLOAT) 
        self.table.setColumnWidth(8, 80)
        self.table.setColumnType(8, AFXTable.FLOAT) 
        self.table.setColumnWidth(9, 80)
        self.table.setColumnType(9, AFXTable.FLOAT)
        self.table.setColumnWidth(10, 80)
        self.table.setColumnType(10, AFXTable.FLOAT)
        self.table.setColumnWidth(11, 80)
        self.table.setColumnType(11, AFXTable.LIST) 
        self.table.setColumnWidth(12, 80)
        self.table.setColumnType(12, AFXTable.LIST)      
        
        
        self.table.setLeadingRowLabels('缠绕形式\t角度\t补强形式\t补强区间上\t补强区间下\t扩孔半径\t滑移系数\t厚度\t纱线宽度\t过渡长度\t位置\t材料名')
        self.table.setStretchableColumn( self.table.getNumColumns()-1 )
        #self.table.setItemEditable(2, 3, False)
        self.table.showHorizontalGrid(True)
        self.table.showVerticalGrid(True)
        
        self.table.setColumnJustify(1,AFXTable.CENTER)
        self.table.setColumnJustify(2,AFXTable.CENTER)
        self.table.setColumnJustify(3,AFXTable.CENTER)
        self.table.setColumnJustify(4,AFXTable.CENTER)
        self.table.setColumnJustify(5,AFXTable.CENTER)
        self.table.setColumnJustify(6,AFXTable.CENTER)
        self.table.setColumnJustify(7,AFXTable.CENTER)
        self.table.setColumnJustify(8,AFXTable.CENTER)
        self.table.setColumnJustify(9,AFXTable.CENTER)
        self.table.setColumnJustify(10,AFXTable.CENTER)
        self.table.setColumnJustify(11,AFXTable.CENTER)
        self.table.setColumnJustify(12,AFXTable.CENTER)
        listId1 = self.table.addList('helix\thelixReaming\tstrengthening\thelix(Friction)\thelixReaming(Friction)\thoop\t')
        
        self.table.setColumnListId(1,listId1) 
        
        listId2 = self.table.addList("up\tdown\t")
        
        self.table.setColumnListId(11,listId2)

        listId4 = self.table.addList("windReinforce\tlayupforce\t")
        
        self.table.setColumnListId(3,listId4)
        
        # modelName = self.form.modelNameKw.getValue()
        # cailiao=mdb.models[modelName].materials.keys()
        
        # for name in cailiao:
            
            # listId3 = self.table.addList(name)
       
        # self.table.setColumnListId(9,listId3) 
        
        

        
        # HFrame_3 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            # pl=0, pr=0, pt=0, pb=0)
        GroupBox_7 = FXGroupBox(p=HFrame_21, text='模型参数', opts=FRAME_GROOVE)
        
        VFrame_41 = FXVerticalFrame(p=GroupBox_7, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)           
        HFrame_4_1 = FXHorizontalFrame(p=VFrame_41, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        self.ComboBox_8 = AFXComboBox(p=HFrame_4_1, ncols=0, nvis=1, text='模型名:', tgt=form.modelNameKw, sel=0)
        self.ComboBox_8.setMaxVisible(10)


        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.ComboBox_8.appendItem(name)
        if not form.modelNameKw.getValue() in names:
            form.modelNameKw.setValue( names[0] )
        msgCount = 40
        form.modelNameKw.setTarget(self)
        form.modelNameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + \
            '.onComboBox_3MaterialsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)'\
            % (msgCount, msgHandler) ) 
            
        VFrame_211 = FXVerticalFrame(p=HFrame_111, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)  

        FXLabel(p=VFrame_211, text='     ', opts=JUSTIFY_RIGHT)
        # AFXTextField(p=VFrame_211, ncols=12, labelText='u1:', tgt=form.u1Kw, sel=0,pl=30)
        # AFXTextField(p=VFrame_211, ncols=12, labelText='b1:', tgt=form.b1Kw, sel=0,pl=30)
        # AFXTextField(p=VFrame_211, ncols=12, labelText='u2:', tgt=form.u2Kw, sel=0,pl=30)
        # AFXTextField(p=VFrame_211, ncols=12, labelText='b2:', tgt=form.b2Kw, sel=0,pl=30)
        #FXButton(p=VFrame_211, text='预算', ic=None,pl=0,opts = BUTTON_NORMAL|LAYOUT_CENTER_X )#tgt=self, sel=self.ID_HELP)            

        self.ComboBox_9 = AFXComboBox(p=HFrame_4_1, ncols=0, nvis=1, text='装配名:', tgt=form.assemblyNameKw, sel=0)
        self.ComboBox_9.setMaxVisible(10)
        self.L_ellipticalheight = AFXTextField(p=HFrame_4_1, ncols=4, labelText='左封头短半轴(mm):', tgt=form.L_ellipticalheightKw, sel=0)
        
        HFrame_4_2 = FXHorizontalFrame(p=VFrame_41, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
################################################################            
        modelName = self.form.modelNameKw.getValue()
        cailiao=mdb.models[modelName].materials.keys()
        
        MATERIAL=''
        for name in cailiao:
            MATERIAL+=str(name)+'\t'
        listId3 = self.table.addList(MATERIAL)
       
        self.table.setColumnListId(12,listId3)
##################################################################
        self.ComboBox_11 = AFXComboBox(p=HFrame_4_2, ncols=0, nvis=1, text='轮廓集(上):', tgt=form.L_setNameKw, sel=0)
        self.ComboBox_11.setMaxVisible(10)

        self.ComboBox_12 = AFXComboBox(p=HFrame_4_2, ncols=0, nvis=1, text='轮廓集(下):', tgt=form.R_setNameKw, sel=0)
        self.ComboBox_12.setMaxVisible(10)
        self.R_ellipticalheight = AFXTextField(p=HFrame_4_2, ncols=4, labelText='右封头短半轴(mm):', tgt=form.R_ellipticalheightKw, sel=0)

 
        # FXMAPFUNC(self, SEL_COMMAND, self.ID_HELP, Wind3DB.helpWindow)
        # FXLabel(p=HFrame_10, text='                                                                              ', opts=JUSTIFY_RIGHT)   
        # FXLabel(p=HFrame_10, text='研制单位：合肥工业大学', opts=JUSTIFY_RIGHT)   


        GroupBox_111 = FXGroupBox(p=VFrame_1, text='数据处理', opts=FRAME_GROOVE)
        HFrame_10 = FXHorizontalFrame(p=GroupBox_111, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
            
        
        # FXButton(p=HFrame_10, text='数据区分', ic=None, tgt=self, sel=self.ID_CHECK) 
        FXLabel(p=HFrame_10, text='  ', ic=None)
        FXButton(p=HFrame_10, text='复制', ic=None, tgt=self, sel=self.ID_COPYTABLE)
        FXLabel(p=HFrame_10, text='  ', ic=None)     
        FXButton(p=HFrame_10, text='正粘贴', ic=None, tgt=self, sel=self.ID_LEFTPASTEABLE)
        FXLabel(p=HFrame_10, text='  ', ic=None)    
        FXButton(p=HFrame_10, text='负粘贴', ic=None, tgt=self, sel=self.ID_RIGHTPASTEABLE)
        FXLabel(p=HFrame_10, text='   ', ic=None)          
        FXButton(p=HFrame_10, text='保存', ic=None, tgt=self, sel=self.ID_SAVE) 
        FXLabel(p=HFrame_10, text='  ', ic=None)
        FXButton(p=HFrame_10, text='导入', ic=None, tgt=self, sel=self.ID_INPUT)     
    
        


        FXMAPFUNC(self, SEL_COMMAND, self.ID_SAVE, Wind3DB.saveToDatabase)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_INPUT, Wind3DB.DatabaseToGui)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_COPYTABLE, Wind3DB.copyTableData)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_LEFTPASTEABLE, Wind3DB.copyTableData)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_RIGHTPASTEABLE, Wind3DB.copyTableData)

        
            
        fileHandler = FileDBFileHandler(form, 'dataBaseName', '(*.par1)')
        fileTextHf = FXHorizontalFrame(p=HFrame_10, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        self.files = AFXTextField(p=fileTextHf, ncols=12, labelText='   文件名:', tgt=form.dataBaseNameKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        self.files.disable()
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)


    def copyTableData(self, sender, sel, ptr):
        
        
        column = 13
        if SELID(sel) == self.ID_COPYTABLE:
            self.layupData=[]
            layupData = self.layupData
            rowNums1=self.table.getNumRows() 
            for i in range(1,rowNums1):                    
                if self.table.isAnyItemInRowSelected(i):
                        column1=self.table.getItemValue(i,1)
                        column2=self.table.getItemValue(i,2)
                        column3=self.table.getItemValue(i,3)
                        column4=self.table.getItemValue(i,4)
                        column5=self.table.getItemValue(i,5)
                        column6=self.table.getItemValue(i,6)
                        column7=self.table.getItemValue(i,7)
                        column8=self.table.getItemValue(i,8)
                        column9=self.table.getItemValue(i,9)
                        column10=self.table.getItemValue(i,10)
                        column11=self.table.getItemValue(i,11)
                        column12=self.table.getItemValue(i,12)
                        layupData.append((column1,column2,column3,column4,column5,column6,column7,column8,column9,column10,column11,column12))
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea("完成表格数据复制")
            mw.writeToMessageArea("layupData=%s"%(layupData))
            
        elif SELID(sel) == self.ID_LEFTPASTEABLE:
            layupData = self.layupData 
            if len(layupData) == 0:
                mw = getAFXApp().getAFXMainWindow()
                mw.writeToMessageArea("重新复制表格")
                return
            countSelected = 0
            rowNums1=self.table.getNumRows() 
            for rowIndex in range(1,rowNums1):                    
                if self.table.isAnyItemInRowSelected(rowIndex):
                    break
            # currentRow=0
            # for currentRow in range(1,rowNums1): 
                # if self.table.getItemValue(rowIndex,1) not in ("helix","helixReaming","strengthening","hoop"):
                    # break
                # msg = "Check the selected row" 
                # raise AbaqusException, msg  
            
            realTable1 = rowIndex + len(layupData)+1
            if realTable1<rowNums1:
                realTable1 = rowNums1
            self.table.setTableSize(realTable1,column)
            
            allRow = rowIndex + len(layupData)
            countLayupData = 0
            for k in range(rowIndex,allRow):
                self.table.setItemText(k,1, layupData[countLayupData][0])
                self.table.setItemText(k,2, layupData[countLayupData][1])
                self.table.setItemText(k,3, layupData[countLayupData][2])            
                self.table.setItemText(k,4, layupData[countLayupData][3])
                self.table.setItemText(k,5, layupData[countLayupData][4])
                self.table.setItemText(k,6, layupData[countLayupData][5])
                self.table.setItemText(k,7, layupData[countLayupData][6])
                self.table.setItemText(k,8, layupData[countLayupData][7])
                self.table.setItemText(k,9, layupData[countLayupData][8])
                self.table.setItemText(k,10, layupData[countLayupData][9])
                self.table.setItemText(k,11, layupData[countLayupData][10])
                self.table.setItemText(k,12, layupData[countLayupData][11])
                countLayupData+=1
            
            #self.layupData=[]
        else:
            layupData = self.layupData 
            if len(layupData) == 0:
                mw = getAFXApp().getAFXMainWindow()
                mw.writeToMessageArea("重新复制表格")
                return
            countSelected = 0
            rowNums1=self.table.getNumRows() 
            for rowIndex in range(1,rowNums1):                    
                if self.table.isAnyItemInRowSelected(rowIndex):
                    break
                # if self.table.getItemValue(rowIndex,1) not in ("helix","helixReaming","strengthening","hoop"):
                    # break                   
                # msg = "Check the selected row" 
                # raise AbaqusException, msg  
            # currentRow=0
            # for currentRow in range(1,rowNums1): 
                # if self.table.getItemValue(rowIndex,1) not in ("helix","helixReaming","strengthening","hoop"):
                    # break
            realTable1 = rowIndex + len(layupData)+1
            if realTable1<rowNums1:
                realTable1=rowNums1
            self.table.setTableSize(realTable1,column)
            
            allRow = rowIndex + len(layupData)
            countLayupData = 0
            for k in range(rowIndex,allRow):
                self.table.setItemText(k,1, layupData[countLayupData][0])
                self.table.setItemText(k,2, layupData[countLayupData][1])
                self.table.setItemText(k,3, layupData[countLayupData][2])            
                self.table.setItemText(k,4, layupData[countLayupData][3])
                self.table.setItemText(k,5, layupData[countLayupData][4])
                self.table.setItemText(k,6, layupData[countLayupData][5])
                self.table.setItemText(k,7, layupData[countLayupData][6])
                self.table.setItemText(k,8, layupData[countLayupData][7])
                self.table.setItemText(k,9, layupData[countLayupData][8])
                self.table.setItemText(k,10, layupData[countLayupData][9])
                self.table.setItemText(k,11, layupData[countLayupData][10])
                self.table.setItemText(k,12, layupData[countLayupData][11])
                if layupData[countLayupData][10] == "up":
                    self.table.setItemText(k,11, "down")
                elif layupData[countLayupData][10] == "down":
                    self.table.setItemText(k,11, "up")
                else:
                    pass
                countLayupData+=1
            
            #self.layupData=[]        
                    
            


    def countTable(self):
        datafilename=self.form.dataBaseNameKw.getValue()
        countTable1 = 1
        fr=file(datafilename,'r')
        for each_line in fr:
            data=each_line.strip().split(',')
            if data[0] == "AFXTable1":
                countTable1+=1
        column = 13
        self.table.setTableSize(countTable1,column)

        #self.table2.setTableSize(countTable2,column)
        


    def DatabaseToGui(self, sender, sel, ptr):
    #设置默认参数数据库文件
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
            if data[0] == "AFXTextField":                           
                if data[1] == "L_segmentationNum":
                    if data[2] == "":
                        pass
                    else:
                        self.form.L_segmentationNumKw.setValue(int(data[2]))
                elif data[1] == "R_segmentationNum":   
                    if data[2] == "":
                        pass
                    else:
                        self.form.R_segmentationNumKw.setValue(int(data[2]))
                elif data[1] == "rotationAngle":
                    self.form.rotationAngleKw.setValue(data[2])
                # elif data[1] == "errorControl":
                    # self.form.errorControlKw.setValue(data[2])
                elif data[1] == "pieceNumber":
                    self.form.pieceNumberKw.setValue(data[2])
                elif data[1] == "approximateSize":
                    self.form.approximateSizeKw.setValue(data[2])             
                elif data[1] == "L_ellipticalheight":
                    self.form.L_ellipticalheightKw.setValue(data[2])
                elif data[1] == "R_ellipticalheight":
                    self.form.R_ellipticalheightKw.setValue(data[2])
                # elif data[1] == "computing_method":
                    # self.form.computing_methodKw.setValue(data[2])
                # elif data[1] == "material_property":
                    # self.form.material_propertyKw.setValue(data[2])
                else:
                    pass
            elif data[0] == "AFXTable1":
                self.table.setItemText(k,1, data[1])
                self.table.setItemText(k,2, data[2])
                self.table.setItemText(k,3, data[3])            
                self.table.setItemText(k,4, data[4])
                self.table.setItemText(k,5, data[5])
                self.table.setItemText(k,6, data[6])
                self.table.setItemText(k,7, data[7])
                self.table.setItemText(k,8, data[8])
                self.table.setItemText(k,9, data[9])
                self.table.setItemText(k,10, data[10])
                self.table.setItemText(k,11, data[11])
                self.table.setItemText(k,12, data[12])
                k+=1
            # elif data[0] == "AFXTable2":
                # self.table2.setItemText(j,1, data[1])
                # self.table2.setItemText(j,2, data[2])
                # self.table2.setItemText(j,3, data[3])            
                # self.table2.setItemText(j,4, data[4])
                # j+=1
                
        self.form.dataBaseNameKw.setValue("")
        mw = getAFXApp().getAFXMainWindow()
        mw.writeToMessageArea("Parameters imported successfully")
                
        

    def saveToDatabase(self, sender, sel, ptr):
        if SELID(sel) == self.ID_SAVE:
            datafilename=self.form.dataBaseNameKw.getValue()
            if datafilename[-5:] !=".par1":
                datafilename+=".par1"
            #thisPath = os.path.abspath(__file__)                                                      
            #thisDir = os.path.dirname(thisPath)                                                              
            #filename= os.path.join(thisDir, 'config_database.dat') 
            f = open(datafilename,'w')
            
            #####################textfield数据保存######################
           
            L_segmentationNumValue = self.L_segmentationNum.getText()
            R_segmentationNumValue = self.R_segmentationNum.getText()
            rotationAngleValue = self.rotationAngle.getText()
            #errorControlValue = self.errorControl.getText()
            pieceNumberValue = self.pieceNumber.getText()
            approximateSizeValue = self.approximateSize.getText()
           
            L_ellipticalheightValue = self.L_ellipticalheight.getText()
            R_ellipticalheightValue = self.R_ellipticalheight.getText()
        
           
            f.writelines("AFXTextField,L_segmentationNum,%s\n"%L_segmentationNumValue)  
            f.writelines("AFXTextField,R_segmentationNum,%s\n"%R_segmentationNumValue)  
            f.writelines("AFXTextField,rotationAngle,%s\n"%rotationAngleValue)  
           
            f.writelines("AFXTextField,pieceNumber,%s\n"%pieceNumberValue)              
            f.writelines("AFXTextField,approximateSize,%s\n"%approximateSizeValue)  
            
###################表格数据保存###########
            #####表格1########
            rowNums1=self.table.getNumRows()   

            for i in range(1,rowNums1):
                column1=self.table.getItemValue(i,1)
                column2=self.table.getItemValue(i,2)
                column3=self.table.getItemValue(i,3)
                column4=self.table.getItemValue(i,4)
                column5=self.table.getItemValue(i,5)
                column6=self.table.getItemValue(i,6)
                column7=self.table.getItemValue(i,7)
                column8=self.table.getItemValue(i,8)
                column9=self.table.getItemValue(i,9)
                column10=self.table.getItemValue(i,10)
                column11=self.table.getItemValue(i,11)
                column12=self.table.getItemValue(i,12)
                f.writelines("AFXTable1,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(column1,column2,column3,column4,column5,column6,column7,column8,column9,column10,column11,column12))
            f.writelines("AFXTextField,L_ellipticalheight,%s\n"%L_ellipticalheightValue)
            f.writelines("AFXTextField,R_ellipticalheight,%s\n"%R_ellipticalheightValue)   
            #####表格2########                
            # rowNums2=self.table2.getNumRows()   

            # for i in range(1,rowNums2):
                # column1=self.table2.getItemValue(i,1)
                # column2=self.table2.getItemValue(i,2)
                # column3=self.table2.getItemValue(i,3)
                # column4=self.table2.getItemValue(i,4)
                # f.writelines("AFXTable2,%s,%s,%s,%s\n"%(column1,column2,column3,column4))
                
            f.close()
            self.form.dataBaseNameKw.setValue("")
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea("save all data to dataBase!\npath:%s\n"%datafilename)



    def processUpdates(self):
        for i in range(1,self.table.getNumRows()):
            if self.table.getItemText(i, 1) =="helix" :
                self.table.setItemEditable(i,2,False)
                self.table.setItemEditable(i,3,False)
                self.table.setItemEditable(i,4,False)
                self.table.setItemEditable(i,5,False)
                self.table.setItemEditable(i,6,False)
                self.table.setItemEditable(i,7,False)
                self.table.setItemEditable(i,8,True)
                self.table.setItemEditable(i,9,True)
                self.table.setItemEditable(i,10,False)
            elif self.table.getItemText(i, 1) =="hoop" :
                self.table.setItemEditable(i,2,False)
                self.table.setItemEditable(i,3,False)
                self.table.setItemEditable(i,4,False)
                self.table.setItemEditable(i,5,False)
                self.table.setItemEditable(i,6,False)
                self.table.setItemEditable(i,7,False)
                self.table.setItemEditable(i,8,True)
                self.table.setItemEditable(i,9,False)
                self.table.setItemEditable(i,10,True)
            elif self.table.getItemText(i, 1) =="helixReaming":
                self.table.setItemEditable(i,2,False)
                self.table.setItemEditable(i,3,False)
                self.table.setItemEditable(i,4,False)
                self.table.setItemEditable(i,5,False)
                self.table.setItemEditable(i,6,True)
                self.table.setItemEditable(i,7,False)
                self.table.setItemEditable(i,8,True)
                self.table.setItemEditable(i,9,True)
                self.table.setItemEditable(i,10,False)
            elif self.table.getItemText(i, 1) =="strengthening":                                                                                  
                self.table.setItemEditable(i,2,True)
                self.table.setItemEditable(i,3,True)
                self.table.setItemEditable(i,4,True)
                self.table.setItemEditable(i,5,True)        
                self.table.setItemEditable(i,6,False)
                self.table.setItemEditable(i,7,False)
                self.table.setItemEditable(i,8,True)
                self.table.setItemEditable(i,9,True)
                self.table.setItemEditable(i,10,False)
                if self.table.getItemText(i, 3) == 'layupforce':
                    self.table.setItemEditable(i,9,False)
                    self.table.setItemEditable(i,2,True)
                else:
                    self.table.setItemEditable(i,9,True)
                    self.table.setItemEditable(i,2,False)
                
            elif self.table.getItemText(i, 1) =="helix(Friction)" :
                self.table.setItemEditable(i,2,False)
                self.table.setItemEditable(i,3,False)
                self.table.setItemEditable(i,4,False)                
                self.table.setItemEditable(i,5,False)
                self.table.setItemEditable(i,6,False)
                self.table.setItemEditable(i,7,True)
                self.table.setItemEditable(i,8,True)
                self.table.setItemEditable(i,9,True)
                self.table.setItemEditable(i,10,False)
            elif self.table.getItemText(i, 1) =="helixReaming(Friction)" :
                self.table.setItemEditable(i,2,False)
                self.table.setItemEditable(i,3,False)
                self.table.setItemEditable(i,4,False)
                self.table.setItemEditable(i,5,False)
                self.table.setItemEditable(i,6,True)
                self.table.setItemEditable(i,7,True)
                self.table.setItemEditable(i,8,True)
                self.table.setItemEditable(i,9,True)
                self.table.setItemEditable(i,10,False)
                #self.table.setItemEditable(i,5,True)
                #self.table.setItemEditable(i,6,True)
            self.table.shadeReadOnlyItems(True)




    def show(self):

        AFXDataDialog.show(self)

        # Register a query on materials
        #
        self.currentModelName = getCurrentContext()['modelName']
        self.form.modelNameKw.setValue(self.currentModelName)
        mdb.models[self.currentModelName].materials.registerQuery(self.updateComboBox_3Materials)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        mdb.models[self.currentModelName].materials.unregisterQuery(self.updateComboBox_3Materials)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_3MaterialsChanged(self, sender, sel, ptr):

        self.updateComboBox_3Materials()
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_3Materials(self):

        modelName = self.form.modelNameKw.getValue()

        # Update the names in the Materials combo
        #
        self.ComboBox_9.clearItems()
        # self.ComboBox_10.clearItems()
        self.ComboBox_11.clearItems()
        self.ComboBox_12.clearItems()
        names = mdb.models[modelName].materials.keys()        
        
        asessemblyname=mdb.models[modelName].rootAssembly.instances.keys()
        if asessemblyname==[]:
            pass
        else:    
            self.form.assemblyNameKw.setValue( asessemblyname[0] )
        
        asessemblyname.sort()
        for name in asessemblyname:
            self.ComboBox_9.appendItem(name)
        if asessemblyname:
            if not self.form.assemblyNameKw.getValue() in asessemblyname:
                self.form.assemblyNameKw.setValue( asessemblyname[0] )
        else:
            self.form.assemblyNameKw.setValue('')
            
############更新材料名 
         
        # for name in names:
            # self.ComboBox_10.appendItem(name)
        # if names:
            # if not self.form.CompositeNameKw.getValue() in names:
                # self.form.CompositeNameKw.setValue( names[0] )
        # else:
            # self.form.CompositeNameKw.setValue('')        


        setNames=mdb.models[modelName].rootAssembly.sets.keys()
##########更新set集名
####外轮廓set集
        setNames.sort()
        for setName in setNames:
            self.ComboBox_11.appendItem(setName)
            
        if setNames:
            if not self.form.L_setNameKw.getValue() in setNames:
                self.form.L_setNameKw.setValue( setNames[0] )
        else:
            self.form.L_setNameKw.setValue('') 

#######全轮廓set集
        for setName in setNames:
            self.ComboBox_12.appendItem(setName)
            
        if setNames:
            if not self.form.R_setNameKw.getValue() in setNames:
                self.form.R_setNameKw.setValue( setNames[0] )
        else:
            self.form.R_setNameKw.setValue('') 
        

        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )





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