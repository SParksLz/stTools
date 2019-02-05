# -*- coding: utf-8 -*-
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



def getMayaWindow() :
    try :
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    except :
        mayaMainWindow = None
    return mayaMainWindow


# class testMenuBar(QMenuBar) :
#     def __init__(self, parent=getMayaWindow()):
#         super(testMenuBar, self).__init__(parent)
#         self.xxxx = parent.findChildren(QMenuBar)[0]
#
#
#         self.setupUI()
#     def setupUI(self):
#         self.menu = QMenu()
#         self.menu.addAction("one")
#         self.menu.addAction("two")
#         self.menu.setTitle("one")
#         self.xxxx.addMenu(self.menu)
#
# testMenuBar().show()


class testMenu(QMenu) :
    def __init__(self, parent = getMayaWindow().findChildren(QMenuBar)[0]):
        super(testMenu, self).__init__(parent)
        self.setTitle("test")
        parent.addMenu(self)
        self.setupUI()
    def setupUI(self):
        self.addAction("one")
        self.addAction("two")





# class tuopan(QSystemTrayIcon) :
#     def __init__(self) :
#         super(tuopan, self).__init__()
#         self.fileControl = file_control()
#         self.iconPath = self.fileControl.getIconDir()
#         self.icon = QIcon(self.iconPath+os.path.sep+"music_A")
#         self.setIcon(self.icon)
#         self.setMenu()
#
#     def setMenu(self) :
#         self.menu = QMenu()
#         self.quitAction = QAction("退出", self, triggered=self.quit)
#         self.menu.addAction(self.quitAction)
#         self.setContextMenu(self.menu)
#
#
#     def quit(self) :
#         self.setVisible(False)
#
#
#
#
#
# if __name__ == "__main__":
#
#     app = QApplication(sys.argv)
#     w = tuopan()
#     w.show()
#     w.showMessage("Now the app is running~~", "click!")
#     sys.exit(app.exec_())