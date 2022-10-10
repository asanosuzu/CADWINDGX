#!/usr/bin/env python
# -*- coding:utf-8 -*-
from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class cylinder_form(AFXForm):


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='createModel',
            objectName='composite', registerQuery=False)
        pickedDefault = ''
        self.pathKw = AFXStringKeyword(self.cmd, 'path', True, '')
        self.pressureValueKw = AFXFloatKeyword(self.cmd, 'pressureValue', True,)
        #self.helixSingleThickKw = AFXFloatKeyword(self.cmd, 'helixSingleThick', True,0.056)
        self.hoopSingleThickKw = AFXFloatKeyword(self.cmd, 'hoopSingleThick', True,)
        # self.helixAngleKw = AFXFloatKeyword(self.cmd, 'helixAngle', True,15)
        self.rotAngleKw = AFXFloatKeyword(self.cmd, 'rotAngle', True,)
        # self.L_polorHoleKw = AFXFloatKeyword(self.cmd, 'L_polorHole', True,)
        # self.R_polarHoleKw = AFXFloatKeyword(self.cmd, 'R_polarHole', True,)
        # self.totalLengthKw = AFXFloatKeyword(self.cmd, 'totalLength', True,)
        # self.L_headLengthKw = AFXFloatKeyword(self.cmd, 'L_headLength', True,)
        # self.R_headLengthKw = AFXFloatKeyword(self.cmd, 'R_headLength', True,)
        self.cylinderLengthKw = AFXFloatKeyword(self.cmd, 'cylinderLength', True,)
        #self.BsplinePrecisionKw = AFXFloatKeyword(self.cmd, 'BsplinePrecision', True,200)
        #self.internalNumKw = AFXFloatKeyword(self.cmd, 'internalNum', True,400)
        #self.smoothCoefficientKw = AFXFloatKeyword(self.cmd, 'smoothCoefficient', True,0.15)
        self.E1Kw = AFXFloatKeyword(self.cmd, 'E1', True,)
        self.E2Kw = AFXFloatKeyword(self.cmd, 'E2', True,)
        self.E3Kw = AFXFloatKeyword(self.cmd, 'E3', True,)        
        self.v12Kw = AFXFloatKeyword(self.cmd, 'v12', True,)
        self.v13Kw = AFXFloatKeyword(self.cmd, 'v13', True,)
        self.v23Kw = AFXFloatKeyword(self.cmd, 'v23', True,)
        self.G12Kw = AFXFloatKeyword(self.cmd, 'G12', True,)
        self.G13Kw = AFXFloatKeyword(self.cmd, 'G13', True,)
        self.G23Kw = AFXFloatKeyword(self.cmd, 'G23', True,)
        self.layUpKw = AFXTableKeyword(self.cmd, 'layUp', True)
        self.layUpKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.layUpKw.setColumnType(1, AFXTABLE_TYPE_STRING)
        self.dataBaseNameKw = AFXStringKeyword(self.cmd, '', False, '')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import cadwindToAbaqusDB
        return cadwindToAbaqusDB.CadwindToAbaqusDB(self)

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
    # buttonText='CadwindToAbaqus_PressureVessels', 
    # object=CadwindToAbaqus_plugin(toolset),
    # messageId=AFXMode.ID_ACTIVATE,
    # icon=None,
    # kernelInitString='import VesselBSplineCadwind2020107',
    # applicableModules=ALL,
    # version='CadwindToAbaqus_PressureVessels 1.0',
    # author='合肥工业大学飞行器实验室',
    # description='2020.10.7创建',
    # helpUrl='N/A'
# )
