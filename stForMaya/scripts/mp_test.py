# -*- coding: utf-8 -*-
import os
import sys

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from shiboken import wrapInstance
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds


def getMayaWindow():
    try:
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    except:
        mayaMainWindow = None
    return mayaMainWindow


def toQtObject(mayaName):
    '''
    Given the name of a Maya UI element of any type,
    return the corresponding QWidget or QAction.
    If the object does not exist, returns None
    '''
    ptr = omui.MQtUtil.findControl(mayaName)
    if ptr is None:
        ptr = omui.MQtUtil.findLayout(mayaName)
    if ptr is None:
        ptr = omui.MQtUtil.findMenuItem(mayaName)
    if ptr is not None:
        return wrapInstance(long(ptr), QObject)


class testWindow(QWidget):
    def __init__(self):
        super(testWindow, self).__init__()

        # self.modelPne = cmds.modelPanel('hhhhhhhhhh', cam='persp')
        # qtObj = toQtObject(self.modelPne)
        self.layoutObjectName = "test_layout"
        self.setLayout(QVBoxLayout())
        self.layout().setObjectName(self.layoutObjectName)
        self.resize(360, 640)
        self.setupUI()

        # self.layout().addWidget(qtObj)

    def setupUI(self):
        # add modelPanel to Qt
        cmds.setParent("%s" % (self.layoutObjectName))

        self.modelPanelName = cmds.modelPanel("playblastModelPanel", cam='persp')

        self.mpPtr = omui.MQtUtil.findControl(self.modelPanelName)
        self.paneLayoutQt = wrapInstance(long(self.mpPtr), QWidget)



        # self.paneLayoutQt.setParent(self)
        self.layout().addWidget(self.paneLayoutQt)
        self.layout().addStretch()

    def closeEvent(self, event) :
        if cmds.modelPanel("playblastModelPanel", exists=True) :
            print "exit"
            print cmds.getPanel(allPanels = True)
            cmds.deleteUI("playblastModelPanel", panel=True)
