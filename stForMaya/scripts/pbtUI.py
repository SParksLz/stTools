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


import pyside2uic as pysideuic
import os
import logging
import xml.etree.ElementTree as xml
from cStringIO import StringIO

import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc



attributeDefaultData = {
                        "Scratchable_latex"         :True,
                        "Top_border_enable"         :True,
                        "Bottom_border_enable"      :True,
                        "Top_text_01"               :"Top Text 01",
                        "Top_Text01_w"              :107,
                        "Top_Text01_showFrame"      :False,
                        "Top_text_02"               :"Top Text 02",
                        "Top_Text_02_w"             :320,
                        "Top_Text02_showFrame"      :False,
                        "Top_text_03"               :"Top Text 03",
                        "Top_Text_03_w"             :533,
                        "Top_Text03_showFrame"      :False,
                        "Bottom_Text01"             :"Bottom Text01",
                        "Bottom_Text01_w"           :107,
                        "Bottom_Text01_showFrame"   :False,
                        "Bottom_Text02"             :"Bottom Text02",
                        "Bottom_Text02_w"           :320,
                        "Bottom_Text02_showFrame"   :False,
                        "Bottom_Text03"             :"Bottom Text03",
                        "Bottom_Text03_w"           :533,
                        "Bottom_Text03_showFrame"   :False

                        }





def getMayaWindow() :
    try :
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    except :
        mayaMainWindow = None
    return mayaMainWindow


class logoLabel(QLabel) :
    def __init__(self):
        super(logoLabel, self).__init__()
        self.setFixedSize(334, 100)
        self.picturePath = "E:\\liuzhen\\Learning\sparksTools\\stForMaya\\scripts\\logo.png"
        self.pic = QPixmap(self.picturePath)
        self.setPixmap(self.pic)


class colorLabel(QLabel) :
    def __init__(self, name, color):
        super(colorLabel, self).__init__()
        self.name = name
        self.setText(self.name)
        self.setFixedHeight(28)
        if  color == "red" :
            self.setStyleSheet("QWidget{background-color:rgb(255, 89, 89);color:rgb(0,0,0)}")
        elif color == "blue" :
            self.setStyleSheet("QWidget{background-color:rgb(0, 196, 255);color:rgb(0,0,0)}")
        elif color == "yellow" :
            self.setStyleSheet("QWidget{background-color:rgb(255, 170, 0);color:rgb(0,0,0)}")
        elif color == "green" :
            self.setStyleSheet("QWidget{background-color:rgb(134, 255, 121);color:rgb(0,0,0)}")


class color_cb(QCheckBox) :
    def __init__(self, name, color):
        super(color_cb, self).__init__()
        self.name = name
        self.color = color
        self.setText(self.name)
        self.setTristate(False)
        if self.color == "yellow":
            self.setStyleSheet("QWidget{background-color:rgb(255, 170, 0);color:rgb(0,0,0)}")
        elif self.color == "green" :
            self.setStyleSheet("QWidget{background-color:rgb(134, 255, 121);color:rgb(0,0,0)}")


class customWidth(QHBoxLayout) :
    def __init__(self, nodeName, widthAttr):
        super(customWidth, self).__init__()
        self.nodeName = nodeName
        self.widthAttr = widthAttr
        self.node = pmc.PyNode(self.nodeName)
        self.width_lineedit = QLineEdit()
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setFixedWidth(245)
        self.width_slider.setMinimum(0)
        self.widthLabel = colorLabel("Width", "red")
        self.regx = QRegExp("^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$")
        self.validator = QRegExpValidator(self.regx, self.width_lineedit)
        self.width_lineedit.setValidator(self.validator)
        self.width_slider.setMaximum(640)

        self.addWidget(self.widthLabel)
        self.addWidget(self.width_lineedit)
        self.addWidget(self.width_slider)

        self.width_lineedit.textEdited.connect(lambda v : self.set_slider_value(float(self.width_lineedit.text())))

        self.width_slider.valueChanged.connect(lambda x : self.set_lineedit_value(self.width_slider.value()))

    def setMaxWidth(self, maxWidth):
        self.width_slider.setMaximum(maxWidth)

    def set_slider_value(self, value):
        if value > self.width_slider.maximum() :
            self.width_slider.setValue(self.width_slider.maximum())
        self.width_slider.setValue(value)

    def set_lineedit_value(self, value):
        self.width_lineedit.setText("%d"%(value))
        self.node.setAttr(self.widthAttr, value)






class text_groupBox(QGroupBox) :
    def __init__(self, nodeName, textAttr, widthAttr, sFAttr, textcb):
        super(text_groupBox, self).__init__()
        self.nodeName = nodeName
        self.node = pmc.PyNode(self.nodeName)
        self.textAttr = textAttr
        self.widthAttr = widthAttr
        self.sfAttr = sFAttr
        self.textcb = textcb


        self.setCheckable(True)
        self.b = pmc.Attribute("%s.%s"%(self.nodeName, self.textcb)).get()
        self.setChecked(self.b)



        self.setTitle(self.textAttr)

        self.setLayout(QVBoxLayout())
        self.text_layout = QHBoxLayout()
        self.width_layout = QHBoxLayout()
        self.textLabel = colorLabel("Text", "blue")
        self.textLineEdit = QLineEdit()
        self.widthWidget = customWidth(self.nodeName, self.widthAttr)
        self.widthLabel = colorLabel("Width", "red")
        self.showFrame_cb = color_cb("Show Frame", "green")
        self.showFrame_cb.setFixedWidth(130)

        self.settDataFromNode()



        self.text_layout.addWidget(self.textLabel)
        self.text_layout.addWidget(self.textLineEdit)

        self.width_layout.addLayout(self.widthWidget)
        self.width_layout.addStretch()

        self.aboveLayout = QHBoxLayout()
        self.setDefAttr_pb = QPushButton("Set Default")
        self.aboveLayout.addWidget(self.showFrame_cb)
        self.aboveLayout.addWidget(self.setDefAttr_pb)
        self.aboveLayout.addStretch()

        self.layout().addLayout(self.aboveLayout)
        self.layout().addLayout(self.text_layout)
        self.layout().addLayout(self.width_layout)

        self.clicked.connect(lambda  : self.test(self.isChecked()))
        self.setDefAttr_pb.clicked.connect(lambda : self.setDefaultData())
        self.showFrame_cb.stateChanged.connect(lambda v : self.checkBox_state(v))
        self.textLineEdit.textChanged.connect(self.lineEdit_text)


    def test(self, b):
        self.node.setAttr(self.textcb, b)


    def settDataFromNode(self, newNode = None):
        text_attr = pmc.Attribute("%s.%s" %(self.nodeName, self.textAttr))
        width_attr = pmc.Attribute("%s.%s" %(self.nodeName, self.widthAttr))
        sf_attr = pmc.Attribute("%s.%s" %(self.nodeName, self.sfAttr))

        self.textLineEdit.setText("%s"%text_attr.get())
        self.widthWidget.width_lineedit.setText("%s"%width_attr.get())
        if sf_attr.get() :
            self.showFrame_cb.setCheckState(Qt.Checked)
        else :
            self.showFrame_cb.setCheckState(Qt.Unchecked)


    def setDefaultData(self):
        self.node.setAttr(self.textAttr, attributeDefaultData[self.textAttr])
        self.node.setAttr(self.widthAttr, attributeDefaultData[self.widthAttr])
        self.node.setAttr(self.sfAttr, attributeDefaultData[self.sfAttr])
        self.settDataFromNode()


    def checkBox_state(self, v):
        self.node.setAttr(self.sfAttr, bool(v))


    def lineEdit_text(self):
        self.node.setAttr(self.textAttr, self.textLineEdit.text())




class settingLayout(QVBoxLayout) :
    def __init__(self, nodename):
        super(settingLayout, self).__init__()
        self.nodename = nodename
        self.sl_cb = color_cb("Scratchable latex", "yellow")
        self.resolution_srtting = QPushButton("Render resolution")
        self.attributeWidget = QWidget()
        self.attributeWidget.setLayout(QVBoxLayout())
        self.add_Attribute()
        self.scollArea = QScrollArea()
        self.scollArea.setWidget(self.attributeWidget)

        self.set_Layout = QHBoxLayout()
        self.set_Layout.addWidget(self.sl_cb)
        self.set_Layout.addWidget(self.resolution_srtting)
        self.addLayout(self.set_Layout)
        self.addWidget(self.scollArea)

        self.resolution_srtting.clicked.connect(lambda : self.setting_signal())


    def add_Attribute(self):
        node = pmc.PyNode(self.nodename)
        attr_list = ["Top_text_01", "Top_text_02", "Top_text_03", "Bottom_Text01", "Bottom_Text02", "Bottom_Text03"]
        if node.hasAttr("Top_text_01") :
            self.tt01_setting_group = text_groupBox(self.nodename, "Top_text_01", "Top_Text01_w", "Top_Text01_showFrame", "Top_Text_01_enable")
            self.attributeWidget.layout().addWidget(self.tt01_setting_group)
        if node.hasAttr("Top_text_02") :
            self.tt02_setting_group = text_groupBox(self.nodename, "Top_text_02", "Top_Text_02_w", "Top_Text02_showFrame", "Top_Text_02_enable")
            self.attributeWidget.layout().addWidget(self.tt02_setting_group)
        if node.hasAttr("Top_text_03") :
            self.tt03_setting_group = text_groupBox(self.nodename, "Top_text_03", "Top_Text_03_w", "Top_Text03_showFrame", "Top_Text_03_enable")
            self.attributeWidget.layout().addWidget(self.tt03_setting_group)
        if node.hasAttr("Bottom_Text01") :
            self.bt01_setting_group = text_groupBox(self.nodename, "Bottom_Text01", "Bottom_Text01_w", "Bottom_Text01_showFrame", "Bottom_Text01_enable")
            self.attributeWidget.layout().addWidget(self.bt01_setting_group)
        if node.hasAttr("Bottom_Text02") :
            self.bt02_setting_group = text_groupBox(self.nodename, "Bottom_Text02", "Bottom_Text02_w", "Bottom_Text02_showFrame", "Bottom_Text02_enable")
            self.attributeWidget.layout().addWidget(self.bt02_setting_group)
        if node.hasAttr("Bottom_Text03") :
            self.bt03_setting_group = text_groupBox(self.nodename, "Bottom_Text03", "Bottom_Text03_w", "Bottom_Text03_showFrame", "Bottom_Text03_enable")
            self.attributeWidget.layout().addWidget(self.bt03_setting_group)

    def setting_signal(self):
        current_node = pmc.PyNode(self.nodename)
        defaultNode = pmc.PyNode("defaultResolution")
        resolutionH = defaultNode.getAttr("height")
        resolutionW = defaultNode.getAttr("width")

        current_node.setAttr("Resolution_Height", resolutionH)
        current_node.setAttr("Resolition_Width", resolutionW)










class mainWindow(QWidget) :
    def __init__(self):
        super(mainWindow, self).__init__()
        self.settingLayoutList = []
        self.selectedNodeName = None
        self.lastSelected = None
        self.setMinimumSize(480, 820)
        self.setMaximumSize(820, 1080)
        self.setLayout(QVBoxLayout())

        self.parentLayout = QHBoxLayout()
        self.settingLayout = QVBoxLayout()
        self.nodeListLayout = QVBoxLayout()

        self.nodeList = QListWidget()


        self.buttonLayout = QHBoxLayout()


        self.createButton = QPushButton("Create")
        self.deleteButton = QPushButton("Delete")
        self.buttonLayout.addWidget(self.createButton)
        self.buttonLayout.addWidget(self.deleteButton)

        self.nodeListLayout.addWidget(self.nodeList)
        self.nodeListLayout.addLayout(self.buttonLayout)
        self.logo = logoLabel()

        self.layout().addWidget(self.logo)
        self.parentLayout.addLayout(self.nodeListLayout)
        self.layout().addLayout(self.parentLayout)

        self.settingListWidget()

        # if self.nodeList.count() > 0 :
        #     print self.nodeList.item(0)
        #     self.settingLayout = settingLayout(self.nodeList.item(0).text())
        #     self.parentLayout.addLayout(self.settingLayout)


        self.createButton.clicked.connect(lambda  : self.createNode())
        self.nodeList.itemClicked.connect(lambda item : self.selected_signal(item))
        self.deleteButton.clicked.connect(lambda : self.deleteSignal())

    def settingListWidget(self):
        pbNodeList = pmc.ls(type = "pbMaskNode")
        if pbNodeList :
            for i in pbNodeList :
                print i.name()
                self.nodeList.addItem(i.name())
                aaa_settingLayout = settingLayout(i.name())
                aaa_frame = QFrame()
                aaa_frame.setObjectName("%s_frame"%i.name())
                aaa_frame.setLayout(aaa_settingLayout)
                self.settingLayoutList.append(settingLayout)
                self.parentLayout.addWidget(aaa_frame)

                aaa_frame.hide()




    def refresh(self):
        self.nodeList.clear()
        pbNodesList = pmc.ls(type="pbMaskNode")
        if pbNodesList :
            for i in pbNodesList :
                self.nodeList.addItem(i.name())



    def createNode(self):
        node = pmc.createNode("pbMaskNode")
        self.nodeDefaultSetting(node)
        self.nodeList.addItem(node.name())
        new_settingLayout = settingLayout(node.name())
        new_frame = QFrame()
        new_frame.setLayout(new_settingLayout)
        new_frame.setObjectName("%s_frame"%node.name())
        self.parentLayout.addWidget(new_frame)
        new_frame.hide()


        # if self.nodeList.count() == 0 :
        #     self.nodeList.addItem("%s" % (node.name()))
        #     self.settingLayout = settingLayout(node.name())
        #     self.parentLayout.addLayout(self.settingLayout)


        self.refresh()

    def nodeDefaultSetting(self, node) :
        node.setAttr("Top_Text_01_enable", 1)
        node.setAttr("Top_Text_02_enable", 1)
        node.setAttr("Top_Text_03_enable", 1)
        node.setAttr("Bottom_Text01_enable", 1)
        node.setAttr("Bottom_Text02_enable", 1)
        node.setAttr("Bottom_Text03_enable", 1)
        node.setAttr("Top_Text01_w", 107)
        node.setAttr("Top_Text_02_w", 320)
        node.setAttr("Top_Text_03_w", 533)
        node.setAttr("Bottom_Text01_w", 107)
        node.setAttr("Bottom_Text02_w", 320)
        node.setAttr("Bottom_Text03_w", 533)
        node.setAttr("Top_border_enable", 1)
        node.setAttr("Bottom_border_enable", 1)
        node.setAttr("Transparency", 0.7)
        node.setAttr("border_height", 35)
        node.setAttr("Top_border_color", [0,0,0])
        node.setAttr("Bottom_border_color", [0,0,0])


    def selected_signal(self, item):
        if self.lastSelected :
            last_frame = self.findChild(QFrame, "%s_frame"%self.lastSelected)
            if last_frame :
                last_frame.hide()

        self.selectedNodeName = item.text()
        selected_Frame = self.findChild(QFrame, "%s_frame"%self.selectedNodeName)
        selected_Frame.show()
        self.lastSelected = self.selectedNodeName



    def deleteSignal(self):
        if self.nodeList.selectedItems() :
            sel_item = self.nodeList.selectedItems()[0]

            node = pmc.listRelatives(sel_item.text(), parent=True, type="transform")
            pmc.delete(node)
            node_frame = self.findChild(QFrame, "%s_frame"%sel_item.text())
            print node_frame

            #remove widget from layout
            self.parentLayout.removeWidget(node_frame)
            node_frame.deleteLater()



            #remove item
            row = self.nodeList.row(sel_item)
            self.nodeList.takeItem(row)






