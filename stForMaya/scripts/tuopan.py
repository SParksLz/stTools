# -*- coding: utf-8 -*-
import os
import sys
from Path import file_control
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *




class tuopan(QSystemTrayIcon) :
    def __init__(self) :
        super(tuopan, self).__init__()
        self.fileControl = file_control()
        self.iconPath = self.fileControl.getIconDir()
        self.icon = QIcon(self.iconPath+os.path.sep+"music_A")
        self.setIcon(self.icon)
        self.setMenu()

    def setMenu(self) :
        self.menu = QMenu()
        self.quitAction = QAction("退出", self, triggered=self.quit)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)


    def quit(self) :
        self.setVisible(False)





if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = tuopan()
    w.show()
    w.showMessage("Now the app is running~~", "click!")
    sys.exit(app.exec_())