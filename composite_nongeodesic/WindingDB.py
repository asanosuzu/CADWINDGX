#!/usr/bin/python
#-*-coding: UTF-8-*-
#-*-coding: mbcs -*- 
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
from wind3_form import wind3_form ###
from rocket_form import rocket_form
from cylinder_form import cylinder_form

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class WindingDB(AFXDataDialog):
    ID_wind3,ID_rocket,ID_cylinder=range(AFXDataDialog.ID_LAST,AFXDataDialog.ID_LAST+3)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):
        self.wind3_form=wind3_form(form.getOwner())###弹出窗口需要用的
        self.rocket_form=rocket_form(form.getOwner())
        self.cylinder_form=cylinder_form(form.getOwner())
        # Construct the base class.

        #
        AFXDataDialog.__init__(self, form, '固体火箭发动机壳体快速建模插件 v1.0',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        #self.form=form    

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
        # AFXDataDialog.__init__(self, form, '复合材料缠绕壳体设计',self.CANCEL)
            

        # cancelBtn = self.getActionButton(self.ID_CLICKED_CANCEL)
        # cancelBtn.setText('关闭')
        VFrame_1 = FXVerticalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)               
        HFrame_0 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0) 

        fileName = os.path.join(thisDir, 'school.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_0, text='', ic=icon)              
            
            
        fileName = os.path.join(thisDir, 'firstP.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_0, text='', ic=icon)
        
      
        

        HFrame_1 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=20, pr=0, pt=20, pb=0)   
     
        FXMAPFUNC(self, SEL_COMMAND, self.ID_wind3,WindingDB.onCmdMybutton_A)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_rocket,WindingDB.onCmdMybutton_B)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_cylinder,WindingDB.onCmdMybutton_C)         
        FXButton(p=HFrame_1, text='  壳体参数化建模  ',tgt=self,sel=self.ID_wind3,opts=BUTTON_NORMAL|LAYOUT_CENTER_X,x=0, y=0, w=0, h=0, pl=0)
        FXLabel(p=HFrame_1, text='                    ', ic=None)
        FXButton(p=HFrame_1, text='Cadwind导入壳体建模',tgt=self,sel=self.ID_cylinder,opts=BUTTON_NORMAL|LAYOUT_CENTER_X,x=5, y=0, w=0, h=0, pl=0)
        FXLabel(p=HFrame_1, text='                    ', ic=None)
        FXButton(p=HFrame_1, text='Cadwind导入一体化壳体建模',tgt=self,sel=self.ID_rocket,opts=BUTTON_NORMAL|LAYOUT_CENTER_X,x=5, y=0, w=0, h=0, pl=0)
        
        fileName = os.path.join(thisDir, 'line.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=VFrame_1, text='', ic=icon)
        
        #FXLabel(p=VFrame_1, text='研制单位：合肥工业大学', ic=None,pt=10,pl=380)
        # fileName = os.path.join(thisDir, 'school.png')
        # icon = afxCreatePNGIcon(fileName)
        # FXLabel(p=VFrame_1, text='', ic=icon,pt=10,pl=380)
        
    def onCmdMybutton_A(self, sender, sel, ptr):
 
        if SELID(sel) == self.ID_wind3:
            self.wind3_form.activate()#激活窗口
            return 1    

    def onCmdMybutton_B(self, sender, sel, ptr):
 
        if SELID(sel) == self.ID_rocket:
            self.rocket_form.activate()
            return 1    
            
    def onCmdMybutton_C(self, sender, sel, ptr):
 
        if SELID(sel) == self.ID_cylinder:
            self.cylinder_form.activate()
            return 1                