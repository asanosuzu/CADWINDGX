#!/usr/bin/env python
# -*- coding:utf-8 -*-
from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class rocket_form(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='yitihua',
            objectName='composite', registerQuery=False)
        pickedDefault = ''
        self.fileNameKw = AFXStringKeyword(self.cmd, 'fileName', True, '')
        self.pressureKw = AFXFloatKeyword(self.cmd, 'pressure', True, )
        self.hxdtKw = AFXFloatKeyword(self.cmd, 'hxdt', True, )
        self.zhuanjiaoKw = AFXFloatKeyword(self.cmd, 'zhuanjiao', True, )
        # self.R0_jikongKw = AFXFloatKeyword(self.cmd, 'R0_jikong', True, 140)
        # self.R0_weipenguanKw = AFXFloatKeyword(self.cmd, 'R0_weipenguan', True, 115)
        self.changduKw = AFXFloatKeyword(self.cmd, 'changdu', True, )
        # self.fengtouchaKw = AFXFloatKeyword(self.cmd, 'fengtoucha', True, 135)
        # self.youfengtouKw = AFXFloatKeyword(self.cmd, 'youfengtou', True, 200)
        self.tschangduKw = AFXFloatKeyword(self.cmd, 'tschangdu', True, )
        self.jinshuneiKw = AFXFloatKeyword(self.cmd, 'jinshunei', True, )
        self.E1Kw = AFXFloatKeyword(self.cmd, 'E1', True, )
        self.E2Kw = AFXFloatKeyword(self.cmd, 'E2', True, )
        self.E3Kw = AFXFloatKeyword(self.cmd, 'E3', True, )
        self.Nu12Kw = AFXFloatKeyword(self.cmd, 'Nu12', True, )
        self.Nu13Kw = AFXFloatKeyword(self.cmd, 'Nu13', True, )
        self.Nu23Kw = AFXFloatKeyword(self.cmd, 'Nu23', True, )
        self.G12Kw = AFXFloatKeyword(self.cmd, 'G12', True, )
        self.G13Kw = AFXFloatKeyword(self.cmd, 'G13', True, )
        self.G23Kw = AFXFloatKeyword(self.cmd, 'G23', True, )
        self.pucengKw = AFXTableKeyword(self.cmd, 'layup', True)
        self.pucengKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.pucengKw.setColumnType(1, AFXTABLE_TYPE_STRING)
        self.dataBaseNameKw = AFXStringKeyword(self.cmd, '', False, '')
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import yitihua2DB
        return yitihua2DB.Yitihua2DB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False
        

                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
# thisPath = os.path.abspath(__file__)
# thisDir = os.path.dirname(thisPath)

# toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
# toolset.registerGuiMenuButton(
    # buttonText='CadWindToAbaqus_RocketEngineHousing', 
    # object=Yitihua2_plugin(toolset),
    # messageId=AFXMode.ID_ACTIVATE,
    # icon=None,
    # kernelInitString='import yitihuaBSplineCadwind2020107',
    # applicableModules=ALL,
    # version='CadWindToAbaqus_RocketEngineHousing 1.0',
    # author='合肥工业大学飞行器实验室',
    # description='2020.10.7创建',
    # helpUrl='N/A'
# )
