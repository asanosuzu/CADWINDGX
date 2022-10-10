
# -* - coding:UTF-8 -*- 
from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class wind3_form(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='mian',
            objectName='composite', registerQuery=False)
        pickedDefault = ''
        #self.fibersWidthKw = AFXStringKeyword(self.cmd, 'fibersWidth',False)
        #self.fibersWidthKw = AFXFloatKeyword(self.cmd, 'fibersWidth',False)
        # self.hoopSingleThickKw = AFXFloatKeyword(self.cmd, 'hoopSingleThick', True)
        # self.singleFiberThickKw = AFXFloatKeyword(self.cmd, 'singleFiberThick', True)
        self.L_segmentationNumKw = AFXIntKeyword(self.cmd, 'L_segmentationNum', True)
        self.R_segmentationNumKw = AFXIntKeyword(self.cmd, 'R_segmentationNum', True)
        self.rotationAngleKw = AFXFloatKeyword(self.cmd, 'rotationAngle', True)
        # self.errorControlKw = AFXFloatKeyword(self.cmd, 'errorControl', True, 1E-006)
        self.pieceNumberKw = AFXFloatKeyword(self.cmd, 'pieceNumber', True)
        self.approximateSizeKw = AFXFloatKeyword(self.cmd, 'approximateSize', True)
        self.L_styleKw = AFXTableKeyword(self.cmd, 'L_style', True)
        self.L_styleKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.L_styleKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.L_styleKw.setColumnType(2, AFXTABLE_TYPE_STRING)
        self.L_styleKw.setColumnType(3, AFXTABLE_TYPE_FLOAT)
        self.L_styleKw.setColumnType(4, AFXTABLE_TYPE_FLOAT)
        self.L_styleKw.setColumnType(5, AFXTABLE_TYPE_FLOAT)
        self.L_styleKw.setColumnType(6, AFXTABLE_TYPE_FLOAT)       
        self.L_styleKw.setColumnType(7, AFXTABLE_TYPE_FLOAT)
        self.L_styleKw.setColumnType(8, AFXTABLE_TYPE_FLOAT)
        self.L_styleKw.setColumnType(9, AFXTABLE_TYPE_FLOAT)
        self.L_styleKw.setColumnType(10, AFXTABLE_TYPE_STRING)
        self.L_styleKw.setColumnType(11, AFXTABLE_TYPE_STRING)
        
        # self.R_styleKw = AFXTableKeyword(self.cmd, 'R_style', True)
        # self.R_styleKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        # self.R_styleKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        # self.R_styleKw.setColumnType(2, AFXTABLE_TYPE_FLOAT)
        # self.R_styleKw.setColumnType(3, AFXTABLE_TYPE_FLOAT)
        self.modelNameKw = AFXStringKeyword(self.cmd, 'modelName', True)
        self.assemblyNameKw = AFXStringKeyword(self.cmd, 'assemblyName', True)

       # self.CompositeNameKw = AFXStringKeyword(self.cmd, 'CompositeName', True)
        self.L_setNameKw = AFXStringKeyword(self.cmd, 'L_setName', True)
        self.R_setNameKw = AFXStringKeyword(self.cmd, 'R_setName', True)
        self.computing_methodKw = AFXStringKeyword(self.cmd, 'computing_method', True)
        self.material_propertyKw = AFXStringKeyword(self.cmd, 'material_property', True)
        #self.typeReinforceKw = AFXStringKeyword(self.cmd, 'typeReinforce', True ,'windReinforce')
        #self.strThickKw = AFXFloatKeyword(self.cmd, 'strThick', True, 0)
        #self.strengtheningAngleKw = AFXFloatKeyword(self.cmd, 'strengtheningAngle', True, 0)
        self.dataBaseNameKw = AFXStringKeyword(self.cmd, '', False, '')
        self.R_ellipticalheightKw=AFXFloatKeyword(self.cmd,'R_ellipticalheight',True)
        self.L_ellipticalheightKw=AFXFloatKeyword(self.cmd,'L_ellipticalheight',True)
        # self.u1Kw = AFXFloatKeyword(self.cmd, 'u1', True)
        # self.b1Kw = AFXFloatKeyword(self.cmd, 'b1', True)
        # self.u2Kw = AFXFloatKeyword(self.cmd, 'u2', True)
        # self.b2Kw = AFXFloatKeyword(self.cmd, 'b2', True)


                




    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import wind3DB
        return wind3DB.Wind3DB(self)

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
        #return True  
        # if self.dataBaseNameKw.getValue()== " ":
            # self.dataBaseNameKw.setValue("None")
        # if self.fibersWidthKw.getValue()<=0:
            # showAFXErrorDialog( self.getCurrentDialog(),
                # '请输入正确的纤维带宽值')
            # return False
        # elif self.hoopSingleThickKw.getValue()<=0:
            # showAFXErrorDialog( self.getCurrentDialog(),
                # '请输入正确的环向单层厚度值')
            # return False
        # elif self.singleFiberThickKw.getValue()<=0:
            # showAFXErrorDialog( self.getCurrentDialog(),
                # '请输入正确的螺旋单层厚度值')
            # return False
        if self.L_segmentationNumKw.getValue()<=0:
            showAFXErrorDialog( self.getCurrentDialog(),
                '请输入正确的切分片数值')      
            return False
        elif self.R_segmentationNumKw.getValue()<=0:
            showAFXErrorDialog( self.getCurrentDialog(),
                '请输入正确的切分片数值')   
            return False                
        elif self.rotationAngleKw.getValue()<=0:
            showAFXErrorDialog( self.getCurrentDialog(),
                '请输入正确的旋转角度值')  
            return False
        elif self.pieceNumberKw.getValue()<=0:
            showAFXErrorDialog( self.getCurrentDialog(),
                '请输入正确的网格分片值') 
            return False
        elif self.L_setNameKw.getValue() == self.R_setNameKw.getValue():
            showAFXErrorDialog( self.getCurrentDialog(),
                '上下set集不能相等') 
            return False
        #elif self.L_styleKw
            
        else:

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
    # buttonText='复合材料插件|复合材料壳体快速建模插件', 
    # object=Wind3_plugin(toolset),
    # messageId=AFXMode.ID_ACTIVATE,
    # icon=None,
    # kernelInitString='import main',
    # applicableModules=ALL,
    # version='1.0',
    # author='合肥工业大学飞行器制造工程系',
    # description='根据参数对气瓶快速化建模的插件',
    # helpUrl='N/A'
# )


