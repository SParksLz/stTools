# -*- coding utf-8 -*-

import os
import sys
try :
    from PySide.QtCore import *
    from PySide.QtGui import *
    from shiboken import wrapInstance
except ImportError :
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc

def getMayaWindow() :
    try :
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    except :
        mayaMainWindow = None
    return mayaMainWindow



class modelPanelWidget(QFrame) :
    def __init__(self):
        super(modelPanelWidget, self).__init__()
        cmds.refresh()
        self.setMaximumSize(640, 360)
        self.setMinimumSize(640, 360)
        self.panelName = "pbModelPanel"
        print cmds.modelPanel("%s" % (self.panelName), exists=True)
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)
        self.layout().setObjectName("%s_Layout" % (self.panelName))
        # cmds.setParent(self.layout().objectName())
        # self.modelPanel = cmds.modelPanel("%s" % (self.panelName),
        #                                   label="ModelPanel")

        self.create_modelPanel()


    def create_modelPanel(self) :
        print self.layout().objectName()
        cmds.setParent(self.layout().objectName())
        self.__modelPanel = cmds.modelPanel("%s" % (self.panelName),
                                            label="ModelPanel")


    # def closeEvent(self, event):
    #     if cmds.modelPanel("%s" % (self.panelName), exists=True) :
    #         cmds.deleteUI(self.panelName, panel=True)



class stPb_Widget(QWidget) :
    def __init__(self):
        super(stPb_Widget, self).__init__()
        self._viewer = modelPanelWidget()
        self.setupUI()
    def setupUI(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._viewer)

        self._buttonA = QPushButton("A")
        self._buttonB = QPushButton("B")
        self._buttonC = QPushButton("C")



        self._buttonGroup = QGroupBox("There is a bunch of buttons~")
        self._buttonGroup.setLayout(QVBoxLayout())
        self._buttonGroup.layout().addWidget(self._buttonA)
        self._buttonGroup.layout().addWidget(self._buttonB)
        self._buttonGroup.layout().addWidget(self._buttonC)

        self.layout().addWidget(self._buttonGroup)
    def closeEvent(self, event):
        if cmds.modelPanel("%s" % (self._viewer.panelName), exists = True) :
            cmds.deleteUI(self._viewer.panelName, panel=True)


