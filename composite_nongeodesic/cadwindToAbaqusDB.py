#!/usr/bin/env python
# -*- coding:utf-8 -*-
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class CadwindToAbaqusDB(AFXDataDialog):
    [ID_SAVE ,ID_INPUT]= range(AFXForm.ID_LAST, AFXForm.ID_LAST+2)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):
        self.form = form 
        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, '纤维缠绕复合材料压力容器CADWind转abaqus快速建模插件',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        VFrame_1 = FXVerticalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
            
        GroupBox_1 = FXGroupBox(p=VFrame_1, text='文件指派', opts=FRAME_GROOVE)
        
        fileHandler = CadwindToAbaqusDBFileHandler(form, 'path', '(*.LAM)')
        fileTextHf = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        AFXTextField(p=fileTextHf, ncols=20, labelText='指定CadWind lam格式的文件', tgt=form.pathKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
            
        GroupBox_2 = FXGroupBox(p=VFrame_1, text='缠绕参数指派', opts=FRAME_GROOVE)
        VAligner_1 = AFXVerticalAligner(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
            
        self.pressure = AFXTextField(p=VAligner_1, ncols=12, labelText='设计爆压/MPa', tgt=form.pressureValueKw, sel=0)
        self.hoopSingleThick = AFXTextField(p=VAligner_1, ncols=12, labelText='筒身环向单层厚度/mm', tgt=form.hoopSingleThickKw, sel=0)
        #AFXTextField(p=VAligner_1, ncols=12, labelText='筒身螺旋单层厚度/mm', tgt=form.helixSingleThickKw, sel=0)
        # AFXTextField(p=VAligner_1, ncols=12, labelText='筒身螺旋缠绕角度/°', tgt=form.helixAngleKw, sel=0)
        self.rotAngle = AFXTextField(p=VAligner_1, ncols=12, labelText='三维模型旋转角度/°', tgt=form.rotAngleKw, sel=0)
        self.cylinderLength = AFXTextField(p=VAligner_1, ncols=12, labelText='筒身长度/mm', tgt=form.cylinderLengthKw, sel=0)
        #HFrame_1 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
        #    pl=0, pr=0, pt=0, pb=0)
        
        GroupBox_3 = FXGroupBox(p=VFrame_1, text='设计参数指派', opts=FRAME_GROOVE|LAYOUT_FILL_X|LAYOUT_FILL_Y)

        TabBook_1 = FXTabBook(p=GroupBox_3, tgt=None, sel=0,
            opts=TABBOOK_NORMAL,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        # tabItem = FXTabItem(p=TabBook_1, text='轮廓参数输入', ic=None, opts=TAB_TOP_NORMAL,
            # x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        # TabItem_1= FXVerticalFrame(p=TabBook_1,
            # opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            # x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            # pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
            
        # VFrame_1 = FXVerticalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            # pl=0, pr=0, pt=0, pb=0)
        # fileName = os.path.join(thisDir, 'pic3.png')
        # icon = afxCreatePNGIcon(fileName)
        # FXLabel(p=TabItem_1, text='', ic=icon)
        
        # VAligner_2 = AFXVerticalAligner(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            # pl=0, pr=0, pt=0, pb=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='左极孔半径/mm(a)', tgt=form.L_polorHoleKw, sel=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='右极孔半径/mm(b)', tgt=form.R_polarHoleKw, sel=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='模型总长度/mm(c)', tgt=form.totalLengthKw, sel=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='左封头长度/mm(d)', tgt=form.L_headLengthKw, sel=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='右封头长度/mm(e)', tgt=form.R_headLengthKw, sel=0)
        # AFXTextField(p=VAligner_2, ncols=12, labelText='筒身长度/mm(f)', tgt=form.cylinderLengthKw, sel=0)
        #AFXTextField(p=VAligner_2, ncols=12, labelText='B样条精度', tgt=form.BsplinePrecisionKw, sel=0)
        #AFXTextField(p=VAligner_2, ncols=12, labelText='间隔数', tgt=form.internalNumKw, sel=0)
        #AFXTextField(p=VAligner_2, ncols=12, labelText='平滑系数', tgt=form.smoothCoefficientKw, sel=0)
        tabItem = FXTabItem(p=TabBook_1, text='工程常数输入', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_2 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        #GroupBox_2 = FXGroupBox(p=TabItem_1, text='工程常数', opts=FRAME_GROOVE)
        VAligner_3 = AFXVerticalAligner(p=TabItem_2, opts=0, x=0, y=0, w=0, h=0,
           pl=0, pr=0, pt=0, pb=0)#对齐布局
        self.E1 = AFXTextField(p=VAligner_3, ncols=12, labelText='E1', tgt=form.E1Kw, sel=0)
        self.E2 = AFXTextField(p=VAligner_3, ncols=12, labelText='E2', tgt=form.E2Kw, sel=0)
        self.E3 = AFXTextField(p=VAligner_3, ncols=12, labelText='E3', tgt=form.E3Kw, sel=0)
        self.v12 = AFXTextField(p=VAligner_3, ncols=12, labelText='v12', tgt=form.v12Kw, sel=0)
        self.v13 = AFXTextField(p=VAligner_3, ncols=12, labelText='v13', tgt=form.v13Kw, sel=0)
        self.v23 = AFXTextField(p=VAligner_3, ncols=12, labelText='v23', tgt=form.v23Kw, sel=0)        
        self.G12 = AFXTextField(p=VAligner_3, ncols=12, labelText='G12', tgt=form.G12Kw, sel=0)
        self.G13 = AFXTextField(p=VAligner_3, ncols=12, labelText='G13', tgt=form.G13Kw, sel=0)
        self.G23 = AFXTextField(p=VAligner_3, ncols=12, labelText='G23', tgt=form.G23Kw, sel=0)
        tabItem = FXTabItem(p=TabBook_1, text='叠层顺序输入', ic=None, opts=TAB_TOP_NORMAL,
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
        self.table = AFXTable(vf, 15, 2, 11, 2, form.layUpKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.table.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE|AFXTable.POPUP_WRITE_TO_FILE)
        self.table.setLeadingRows(1)
        self.table.setLeadingColumns(1)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnType(1, AFXTable.TEXT)
        self.table.setLeadingRowLabels('螺旋缠绕循环(一个循环两层)   环向缠绕单层\t')
        self.table.setStretchableColumn( self.table.getNumColumns()-1 )
        #引入表格下拉选项
        self.table.setColumnJustify(1,AFXTable.CENTER)
        listId1 = self.table.addList('HelixLoop\tHoop\t')
        self.table.setColumnType(1,AFXTable.LIST)
        self.table.setColumnListId(1,listId1)             
        
        
        self.table.showHorizontalGrid(True)
        self.table.showVerticalGrid(True)





        GroupBox_111 = FXGroupBox(p=VFrame_1, text='数据处理', opts=FRAME_GROOVE)
        HFrame_10 = FXHorizontalFrame(p=GroupBox_111, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
            


        FXButton(p=HFrame_10, text='保存', ic=None, tgt=self, sel=self.ID_SAVE) 
        FXButton(p=HFrame_10, text='导入', ic=None, tgt=self, sel=self.ID_INPUT)            


        FXMAPFUNC(self, SEL_COMMAND, self.ID_SAVE, CadwindToAbaqusDB.saveToDatabase)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_INPUT, CadwindToAbaqusDB.DatabaseToGui)
        
        
        fileHandler = FileDBFileHandler(form, 'dataBaseName', '(*.par2)')
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



    def countTable(self):
        datafilename=self.form.dataBaseNameKw.getValue()
        countTable1,countTable2 = 1,1
        column = 2
        f=file(datafilename,'r')
        for each_line in f:
            data=each_line.strip().split(',')
            if data[0] == "P2_AFXTable1":
                countTable1+=1
        if countTable1 == 1:
            countTable1+=1
        self.table.setTableSize(countTable1,column)

        


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
            if data[0] == "P2_AFXTextField":
            
                if data[1] == "pressure":
                    self.form.pressureValueKw.setValue(data[2])
                elif data[1] == "rotAngle":
                    self.form.rotAngleKw.setValue(data[2])
                elif data[1] == "cylinderLength":
                    self.form.cylinderLengthKw.setValue(data[2])
                elif data[1] == "E1":
                    self.form.E1Kw.setValue(data[2])
                elif data[1] == "E2":
                    self.form.E2Kw.setValue(data[2])
                elif data[1] == "E3":
                    self.form.E3Kw.setValue(data[2])
                elif data[1] == "v12":
                    self.form.v12Kw.setValue(data[2])
                elif data[1] == "v13":
                    self.form.v13Kw.setValue(data[2])
                elif data[1] == "v23":
                    self.form.v23Kw.setValue(data[2])
                    
                elif data[1] == "G12":
                    self.form.G12Kw.setValue(data[2])
                elif data[1] == "G13":
                    self.form.G13Kw.setValue(data[2])
                elif data[1] == "G23":
                    self.form.G23Kw.setValue(data[2])                                        
                else:
                    pass
            elif data[0] == "P2_AFXTable1":
                self.table.setItemText(k,1, data[1])
                k+=1

        
        self.form.dataBaseNameKw.setValue("")        
        mw = getAFXApp().getAFXMainWindow()
        mw.writeToMessageArea("Parameters imported successfully")
                
        

    def saveToDatabase(self, sender, sel, ptr):
        if SELID(sel) == self.ID_SAVE:
            datafilename=self.form.dataBaseNameKw.getValue()
            if datafilename[-5:] !=".par2":
                datafilename+=".par2"
            #thisPath = os.path.abspath(__file__)                                                      
            #thisDir = os.path.dirname(thisPath)                                                              
            #filename= os.path.join(thisDir, 'config_database.dat') 
            f = open(datafilename,'w')
            
            #####################textfield数据保存######################
            pressureValue = self.pressure.getText()
            rotAngleValue = self.rotAngle.getText()
            cylinderLengthValue = self.cylinderLength.getText()
            E1Value = self.E1.getText()
            E2Value = self.E2.getText()
            E3Value = self.E3.getText()
            v12Value = self.v12.getText()
            v13Value = self.v13.getText()
            v23Value = self.v23.getText()
            G12Value = self.G12.getText()
            G13Value = self.G13.getText()
            G23Value = self.G23.getText()

            
        
            f.writelines("P2_AFXTextField,pressure,%s\n"%pressureValue)  
            f.writelines("P2_AFXTextField,rotAngle,%s\n"%rotAngleValue)
            f.writelines("P2_AFXTextField,cylinderLength,%s\n"%cylinderLengthValue)  
            f.writelines("P2_AFXTextField,E1,%s\n"%E1Value)  
            f.writelines("P2_AFXTextField,E2,%s\n"%E2Value)  
            f.writelines("P2_AFXTextField,E3,%s\n"%E3Value)              
            f.writelines("P2_AFXTextField,v12,%s\n"%v12Value)  
            f.writelines("P2_AFXTextField,v13,%s\n"%v13Value)
            f.writelines("P2_AFXTextField,v23,%s\n"%v23Value)
            
            f.writelines("P2_AFXTextField,G12,%s\n"%G12Value)
            f.writelines("P2_AFXTextField,G13,%s\n"%G13Value)
            f.writelines("P2_AFXTextField,G23,%s\n"%G23Value)
            

###################表格数据保存###########
            #####表格1########
            rowNums1=self.table.getNumRows()   

            for i in range(1,rowNums1):
                column1=self.table.getItemValue(i,1)
                f.writelines("P2_AFXTable1,%s\n"%column1)
                
            f.close()
            self.form.dataBaseNameKw.setValue("")   
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea("save all data to dataBase!\npath:%s\n"%datafilename)        



###########################################################################
# Class definition
###########################################################################

class CadwindToAbaqusDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.pathKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, CadwindToAbaqusDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.pathKw, self.readOnlyKw,
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