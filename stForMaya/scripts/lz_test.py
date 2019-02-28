import os
import shiboken2

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

try:
    import maya.cmds as cmds
    import maya.OpenMayaUI as mui
    isMaya = True
except ImportError:
    isMaya = False


__all__ = ["ModelPanelWidget"]

# def currentModelPanel():
#     """
#     :rtype: str or None
#     """
#     currentPanel = cmds.getPanel(withFocus=True)
#     currentPanelType = cmds.getPanel(typeOf=currentPanel)
#
#     if currentPanelType not in ['modelPanel']:
#         return None
#
#     return currentPanel



class viewGroup(QGroupBox) :
    def __init__(self, name):
        super(viewGroup, self).__init__(name)
        self.name = name
        self._settingButton = QPushButton("Setting")
        self.resize(640, 360)
        self.setFixedSize(640, 360)
        self.setLayout(QVBoxLayout())
        self._mainLayout = self.layout()
        self._mainLayout.setObjectName("%s_mainLayout"%(self.name))
        cmds.setParent(self._mainLayout.objectName())
        self.modelName = cmds.modelEditor("%sEditor"%(self.name))
        self.modelptr = mui.MQtUtil.findControl(self.modelName)
        self._modelQt = shiboken2.wrapInstance(long(self.modelptr), QWidget)

        self._mainLayout.layout().addWidget(self._modelQt)
        self._mainLayout.layout().addWidget(self._settingButton)








class ModelPanelWidget(QWidget):


    def __init__(self,name="modelView4Pb"):
        super(ModelPanelWidget, self).__init__()
        # self.setMaximumWidth(640)
        self.setFixedWidth(660)
        self._currentdir = dir_path = os.path.dirname(__file__)
        self._iconPath = os.path.join(os.path.dirname(self._currentdir), "icons")
        self._titlePic = os.path.join(self._iconPath, "title_A.jpg")
        self.modelViewName = name
        self._viewGroup = viewGroup(self.modelViewName)
        self.buildUI()

    def buildUI(self):
        #icon
        self._picFrame = QFrame()
        self._pic = QIcon(self._titlePic)

        self._picFrame.setWindowIcon(self._pic)
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(self._picFrame)
        self.layout().addWidget(self._viewGroup)




        #option group
        self._pathGroup = QGroupBox("Output directory")
        self._optionGroup = QGroupBox("Option")
        self.layout().addWidget(self._pathGroup)
        self.layout().addWidget(self._optionGroup)

        self._pathGroup.setLayout(QHBoxLayout())
        self._optionGroup.setLayout(QHBoxLayout())

        self._outputOptionLayout = QVBoxLayout()



        #------------------viewOption------------------
        self._option1 = QCheckBox("option1")
        self._option2 = QCheckBox("option2")
        self._option3 = QCheckBox("option3")

        self._cameraLayout = QHBoxLayout()
        self._cameraLabel = QLabel("Camera : ")
        self._cameraCombox = QComboBox()
        self._cameraLayout.addWidget(self._cameraLabel)
        self._cameraLayout.addWidget(self._cameraCombox)


        self._viewOptionLayout = QVBoxLayout()
        self._viewOptionLayout.addLayout(self._cameraLayout)
        self._viewOptionLayout.addWidget(self._option1)
        self._viewOptionLayout.addWidget(self._option2)
        self._viewOptionLayout.addWidget(self._option3)
        self._viewOptionLayout.addStretch()


        #------------------outputOption------------------
        self.timeRangeLabel = QLabel("Time range:")
        self.timeSlidercb = QCheckBox("Time Slider")
        self.seCb = QCheckBox("Start/End")
        self.timeRangeLayout = QHBoxLayout()
        self.timeRangeLayout.addWidget(self.timeRangeLabel)
        self.timeRangeLayout.addWidget(self.timeSlidercb)
        self.timeRangeLayout.addStretch()
        self.timeRangeLayout.addWidget(self.seCb)



        self._startLabel = QLabel("Start time :")
        self._endLabel = QLabel("End time :")
        self._startEditor = QLineEdit()
        self._endEditor = QLineEdit()




        self._startLayout = QHBoxLayout()
        self._startLayout.addWidget(self._startLabel)
        self._startLayout.addWidget(self._startEditor)
        self._startLayout.addStretch()
        self._endLayout = QHBoxLayout()
        self._endLayout.addWidget(self._endLabel)
        self._endLayout.addWidget(self._endEditor)
        self._endLayout.addStretch()
        # self._frameRangeLayout.addWidget(self._startLabel)
        # self._frameRangeLayout.addWidget(self._startEditor)
        # self._frameRangeLayout.addWidget(self._endLabel)
        # self._frameRangeLayout.addWidget(self._endEditor)
        # self._frameRangeLayout.addStretch()

        self._outputOptionLayout.addLayout(self.timeRangeLayout)
        self._outputOptionLayout.addLayout(self._startLayout)
        self._outputOptionLayout.addLayout(self._endLayout)
        self._outputOptionLayout.addStretch()
        # self._outputOptionLayout.addLayout(self._frameRangeLayout)




        #----------------------------------------------------
        self._optionGroup.layout().addLayout(self._viewOptionLayout)
        self._optionGroup.layout().addStretch()
        self._optionGroup.layout().addLayout(self._outputOptionLayout)



    def closeEvent(self, event):
        if cmds.modelEditor("%sEditor"%(self.modelViewName), query=True, exists=True) :
            cmds.deleteUI("%sEditor"%(self.modelViewName))

        print cmds.modelEditor("%sEditor"%(self.modelViewName), query=True, exists=True)







    # def setModelPanelOptions(self):
    #
    #     modelPanel = self.name()

        # cmds.modelEditor(modelPanel, edit=True, allObjects=False)
        # cmds.modelEditor(modelPanel, edit=True, grid=True)
        # cmds.modelEditor(modelPanel, edit=True, av=False)
        # cmds.modelEditor(modelPanel, edit=True, dynamics=False)
        # cmds.modelEditor(modelPanel, edit=True, activeOnly=False)
        # cmds.modelEditor(modelPanel, edit=True, manipulators=False)
        # # maya.cmds.modelEditor(modelPanel, edit=True, headsUpDisplay=False)
        # cmds.modelEditor(modelPanel, edit=True, selectionHiliteDisplay=False)
        #
        # cmds.modelEditor(modelPanel, edit=True, polymeshes=True)
        # cmds.modelEditor(modelPanel, edit=True, nurbsSurfaces=True)
        # cmds.modelEditor(modelPanel, edit=True, subdivSurfaces=True)
        # cmds.modelEditor(modelPanel, edit=True, displayTextures=True)
        # # maya.cmds.modelEditor(modelPanel, edit=True, width=640)
        # # maya.cmds.modelEditor(modelPanel, edit=True, height=360)
        # cmds.modelEditor(modelPanel, edit=True, displayTextures=True)
        # cmds.modelEditor(modelPanel, edit=True, displayAppearance="smoothShaded")

    #     currentModelPanelx = currentModelPanel()
    #
    #     if currentModelPanelx:
    #         camera = cmds.modelEditor(currentModelPanelx, query=True, camera=True)
    #         displayLights = cmds.modelEditor(currentModelPanelx, query=True, displayLights=True)
    #         displayTextures = cmds.modelEditor(currentModelPanelx, query=True, displayTextures=True)
    #
    #         cmds.modelEditor(modelPanel, edit=True, camera=camera)
    #         cmds.modelEditor(modelPanel, edit=True, displayLights=displayLights)
    #         cmds.modelEditor(modelPanel, edit=True, displayTextures=displayTextures)
    #
    # def name(self):
    #     return self._modelPanel
    #
    # def modelPanel(self):
    #     ptr = mui.MQtUtil.findControl(self._modelPanel)
    #     return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
    #
    # def barLayout(self):
    #     name = maya.cmds.modelPanel(self._modelPanel, query=True, barLayout=True)
    #     ptr = mui.MQtUtil.findControl(name)
    #     return shiboken2.wrapInstance(long(ptr), QtCore.QObject)
    #
    # def hideBarLayout(self):
    #     self.barLayout().hide()
    #
    # def hideMenuBar(self):
    #     maya.cmds.modelPanel(self._modelPanel, edit=True, menuBarVisible=False)



# if __name__ == "__main__":
#     widget = ModelPanelWidget(None, "modelPanel")
#     widget.show()