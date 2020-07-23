import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

'''
this .py file shows how to create a grid listwidget with icon
'''


if __name__  == "__main__" :
    app = QApplication(sys.argv)
    testWindow = QWidget()
    testListWidget = QListWidget()
    testListWidget.setFlow(QListView.LeftToRight)
    testListWidget.setResizeMode(QListView.Adjust)
    testListWidget.setGridSize(QSize(128,128))
    testListWidget.setIconSize(QSize(115,115))
    testListWidget.setSpacing(2)
    testListWidget.setViewMode(QListView.IconMode)
    itemA = QListWidgetItem()
    # frameA = QFrame()
    # frameA.setWindowIcon(QIcon(r"Z:\A_Project\sparks_sg\icons\a.jpg"))
    itemA.setIcon(QIcon(r"Z:\A_Project\sparks_sg\icons\a.jpg"))

    # itemA.setText("AAA")
    itemB = QListWidgetItem()
    # frameB = QFrame()
    # frameB.setWindowIcon(QIcon(r"Z:\A_Project\sparks_sg\icons\b.jpg"))
    itemB.setIcon(QIcon(r"Z:\A_Project\sparks_sg\icons\b.jpg"))
    # itemB.setText("BBB")
    itemC = QListWidgetItem()
    # frameC = QFrame()
    # frameC.setWindowIcon(QIcon(r"Z:\A_Project\sparks_sg\icons\c.jpg"))
    itemC.setIcon(QIcon(r"Z:\A_Project\sparks_sg\icons\c.jpg"))
    # itemC.setText("CCC")

    testListWidget.addItem(itemA)
    # testListWidget.setWidgetItem(itemA, frameA)
    testListWidget.addItem(itemB)
    # testListWidget.setWidgetItem(itemB, frameB)
    testListWidget.addItem(itemC)
    # testListWidget.setWidgetItem(itemC, frameC)

    testLayout = QVBoxLayout()
    testLayout.addWidget(testListWidget)

    testWindow.setLayout(testLayout)




    testWindow.resize(640,360)
    testWindow.show()

    sys.exit(app.exec_())