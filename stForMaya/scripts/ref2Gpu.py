import os
import sys
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pmc
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

def getMayaWindow() :
    try :
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    except :
        mayaMainWindow = None
    return mayaMainWindow


# class listStruct(QAbstractListModel) :
#     def __init__(self, refList = [], parent=None):
#         super(listStruct, self).__init__()
#         self.refList = refList
#
#     def rowCount(self, parent):
#         return len(self.refList)
#
#     def data(self, index, role):
#
#         if role == Qt.DisplayRole :
#             row = index.row()
#             value = self.refList[row]
#             return value.name()





class cuslabel(QLabel) :
    def __init__(self):
        super(cuslabel, self).__init__()
        self.setStyleSheet("QWidget{background-color:rgb(0, 196, 255);color:rgb(0,0,0)}")


class listItem(QWidget) :
    def __init__(self, type, name) :
        super(listItem, self).__init__()
        self.name = name
        self.type = type
        self.setObjectName("{0}__{1}__{2}".format(self.type, self.name, "list"))
        print self.objectName()
        self.setLayout(QHBoxLayout())
        self.setupUi()


    def setupUi(self) :
        if self.type == "reference" :
            self.status = True
            self.switchButton = QPushButton(">>>")
            self.switchButton.setObjectName("{0}__{1}__{2}".format(self.type, self.name, "pushButton"))
            self.label = cuslabel()
            print self.name
            self.label.setText(self.name)
            self.label.setObjectName("{0}__{1}__{2}".format(self.type, self.name, "label"))
            self.layout().addWidget(self.label)
            self.layout().addWidget(self.switchButton)


        elif self.type == "gpuCache" :
            self.status = False
            self.switchButton = QPushButton("<<<")
            self.switchButton.setObjectName("{0}__{1}__{2}".format(self.type, self.name, "pushButton"))
            self.label = cuslabel()
            self.label.setText(self.name)
            self.label.setObjectName("{0}__{1}__{2}".format(self.type, self.name, "label"))
            self.overridePushButton = QPushButton("Override")
            self.layout().addWidget(self.switchButton)
            self.layout().addWidget(self.label)
            self.layout().addWidget(self.overridePushButton)
            self.setToDisabled()

        else :

            print "unknown type"

    def setToDisabled(self):
        label = self.findChild(QLabel, "{0}__{1}__{2}".format(self.type, self.name, "label"))
        label.setStyleSheet("QWidget{background-color:rgb(125, 125, 125);color:rgb(0,0,0)}")
        self.setDisabled(True)
        self.status = False


    def setToEnabled(self):
        label = self.findChild(QLabel, "{0}__{1}__{2}".format(self.type, self.name, "label"))
        label.setStyleSheet("QWidget{background-color:rgb(0, 196, 255);color:rgb(0,0,0)}")
        self.setDisabled(False)
        self.status = True


class objectList(QListWidget) :
    def __init__(self, type=None) :
        super(objectList, self).__init__()
        self.type=type

    def addWidgetItems(self, name) :
        self.name = name
        self._itemFrame = QListWidgetItem(self)
        self._itemFrame.setSizeHint(QSize(90, 34))
        self._cWidgetItem = listItem(self.type, self.name)
        self.setItemWidget(self._itemFrame, self._cWidgetItem)
        return self._cWidgetItem


    # def setToDisabled(self, boolx):
    #     label = self.findChild(QLabel, "{}_{}_{}".format(self.type, self.name, "label"))
    #     label.setStyleSheet("QWidget{background-color:rgb(125, 125, 125);color:rgb(0,0,0)}")
    #     self.setDisabled(True)
    #     boolx = False
    #
    #
    # def setToEnabled(self):
    #     label = self.findChild(QLabel, "{}_{}_{}".format(self.type, self.name, "label"))
    #     label.setStyleSheet("QWidget{background-color:rgb(0, 196, 255);color:rgb(0,0,0)}")
    #     self.setDisabled(False)
    #     boolx = True




class referenceList(objectList) :
    def __init__(self) :
        super(referenceList, self).__init__()
        self.type = "reference"
        self.status = True

    def setupUi(self) :
        pass

    def ref_switch(self):
        if self.status == True :

            self.setToDisabled()
        else :
            self.setToEnabled()



class gpuCacheList(objectList) :
    def __init__(self) :
        super(gpuCacheList, self).__init__()
        self.type = "gpuCache"
        self.status = False

    def setupUi(self) :

        pass
    def gc_switch(self):

        if self.status == True:

            self.setToDisabled()
        else:
            self.setToEnabled()

class mainWidget(QWidget) :
    def __init__(self) :
        super(mainWidget, self).__init__()
        self.setWindowTitle("reference2GPUCache")
        self.setLayout(QVBoxLayout())
        self.setFixedSize(450, 680)
        self.TAcore = taCore()
        self.buildWindow()


    def buildWindow(self) :

        #set main layout
        self._topLayout = QHBoxLayout()
        self._midLayout = QHBoxLayout()
        self._button_beta = QPushButton()
        self._midChildLayout_ref = QVBoxLayout()
        self._midChildLayout_gc = QVBoxLayout()
        self._midLayout.addLayout(self._midChildLayout_ref)
        self._midLayout.addLayout(self._midChildLayout_gc)
        self._bottomLayout = QVBoxLayout()

        #set widget
        self._refTitle = QLabel("Reference")
        self._refWidget = referenceList()
        self._gcTitle = QLabel("GPU Cache")
        self._gcwWidget = gpuCacheList()

        self._refList = self.TAcore.getAllRefNode()
        if self._refList is not None :
            print self._refList
            for ref in self._refList :
                if not cmds.referenceQuery(ref.name(), isLoaded=True) :
                    ref_fileName = cmds.referenceQuery(ref.name(), filename=True)
                    cmds.file(ref_fileName, loadReferenceDepth="asPrefs", loadReference=ref.name())
                self.rf_list = self._refWidget.addWidgetItems(ref.name())
                if not cmds.referenceQuery(self.rf_list.name, isLoaded=True) :
                    self.rf_list.setToDisabled()
                self.gc_list = self._gcwWidget.addWidgetItems(ref.name())
                self.rfButton = self.rf_list.switchButton
                self.gcButton = self.gc_list.switchButton
                # print self.gcButton,"_",self.rfButton

                self.rfButton.clicked.connect(self.mainSlot)
                self.gcButton.clicked.connect(self.mainSlot)


        #---------
        self._midChildLayout_ref.addWidget(self._refTitle)
        self._midChildLayout_ref.addWidget(self._refWidget)

        self._midChildLayout_gc.addWidget(self._gcTitle)
        self._midChildLayout_gc.addWidget(self._gcwWidget)

        self.layout().addLayout(self._topLayout)
        self.layout().addLayout(self._midLayout)
        self.layout().addLayout(self._bottomLayout)

    def mainSlot(self):
        sender = self.sender()
        sender_objectname = sender.objectName()

        print "*"*20
        print sender_objectname
        print "*" * 20

        parent = sender.parentWidget()


        if parent.type == "reference" :
            another_object_name = "{0}__{1}__{2}".format("gpuCache", sender_objectname.split("__")[1],sender_objectname.split("__")[-1])
            print another_object_name
            another_object = self.findChild(QPushButton, another_object_name)
            self.TAcore.switch(sender, another_object)


        elif parent.type == "gpuCache" :

            another_object_name = "{0}__{1}__{2}".format("reference", sender_objectname.split("__")[1],sender_objectname.split("__")[-1])
            another_object = self.findChild(QPushButton, another_object_name)
            self.TAcore.switch(sender, another_object)


class taCore(object) :
    def __init__(self) :
        self.filePath = cmds.file(query=True, sn=True)
        self.projectName = os.path.dirname(os.path.dirname(self.filePath))
        self.gpucache_desPath = os.path.join(self.projectName, "cache/alembic")

        if self.filePath == '' :

            self.projectName = os.path.dirname(os.path.dirname(self.filePath))
            self.gpucache_desPath = os.path.join(self.projectName, "cache/alembic")
            print self.gpucache_desPath
            self.geocache_desPath = os.path.join(self.projectName, "cache/nCache")
            print self.geocache_desPath
    def getpartofname(self):
        fullfileName = os.path.basename(self.filePath)
        fileNameText = os.path.splitext(fullfileName)[0]

        partOfname = "".join(fileNameText.split("_"))

        return partOfname




    def getAllRefNode(self):
        refList = pmc.ls(references=True)
        return refList


    def getNodesFromRef(self, refName) :
        topNode = pmc.PyNode(refName).nodes()[0]
        print topNode

        return topNode.name()


    # def getGeoFromRef(self, refList):
    #     asset_dir = {}
    #     nodeList = refList.nodes()
    #     for node in nodeList :
    #         if node.hasAttr("asset_name") :
    #             asset_dir[node.getAttr("asset_name")]


    def getAllgpuCache(self):
        gpu_dir = {}
        if os.path.exists(self.gpucache_desPath) :
            all_gpuCache = os.listdir(self.gpucache_desPath)
            return all_gpuCache
        else :
            return None

    def getAllgeoCache(self):
        if os.path.exists(self.geocache_desPath) :

            all_geoCache = os.listdir(self.geocache_desPath)
            return all_geoCache
        else :
            return None

    def getgpuCacheByname(self):
        pass


    def exportGpuCache(self, refName) :
        print ":"*20
        print refName
        print ":" * 20
        node = pmc.PyNode(refName)
        print node.nodes()
        name = self.getpartofname()
        gpuCachename = "{0}__{1}__{2}".format(refName, "gpuCache", name)
        desPath = os.path.join(self.gpucache_desPath, gpuCachename)
        targetFile = desPath+".abc"
        self.getNodesFromRef(refName)
        topNodeName = self.getNodesFromRef(refName)
        print targetFile
        print os.path.exists(targetFile)
        if not os.path.exists(targetFile) :
            start = str(pmc.playbackOptions(q=1, min=1))
            end = str(pmc.playbackOptions(q=1, max=1))
            mel.eval( 'gpuCache -startTime '+start+' -endTime '+end+' -simulationRate 2 -optimize -optimizationThreshold 10000 -useBaseTessellation -dataFormat ogawa -directory "' + self.gpucache_desPath + '" -fileName "' + gpuCachename + '" ' + topNodeName)
            self.importGpuCache(gpuCachename, targetFile)

        else :
            self.importGpuCache(gpuCachename, targetFile)


    def removeGpuCache(self, refName) :
        gcnode = cmds.ls("{0}__gpuCache*".format(refName))[0]
        cmds.delete(gcnode)


    def importGpuCache(self, tf, path):
        print tf
        if cmds.objExists(tf) :
            gpuNode = pmc.PyNode(tf)
            gpuNode.setAttr("cacheFileName", path)
        else :
            gpuNodeName = cmds.createNode("gpuCache")
            gpuNode = pmc.PyNode(gpuNodeName)
            transNode = gpuNode.listRelatives(parent=True)[0]
            transNode.rename(tf)


            gpuNode.setAttr("cacheFileName", path)

    def exportGeoCache(self) :
        pass



    def unloadReference(self, refName) :
        nodeName = refName
        # print nodeName
        fileName = cmds.referenceQuery(nodeName, filename=True)
        # print fileName
        cmds.file(fileName, unloadReference=nodeName)


    def loadReference(self, refName) :
        nodeName = refName
        fileName = cmds.referenceQuery(nodeName, filename = True)
        cmds.file(fileName, loadReferenceDepth="asPrefs", loadReference=nodeName)

    def switch(self, selfButton, anotherbutton):
        sButton = selfButton
        aButton = anotherbutton
        sParent = sButton.parentWidget()
        print sButton
        print aButton
        aParent = aButton.parentWidget()

        sAssetname = sButton.objectName().split("__")[1]
        if sParent.type == "reference" :
            self.exportGpuCache(sAssetname)
            self.unloadReference(sAssetname)
        elif sParent.type == "gpuCache" :
            self.removeGpuCache(sAssetname)
            self.loadReference(sAssetname)
        sParent.setToDisabled()
        aParent.setToEnabled()

        # gc_list = "{0}_{1}_{2}".format("gpuCache", objectName.split("_")[1], objectName.split("_")[2])

        # print aaa
        # gc_object = ppObject.findChild(listItem, gc_list)
        # print gc_list
        # print gc_object




    def switchToReference(self, selfButton, anotherbutton) :
        print selfButton.objectName()
        print anotherbutton.objectName()


    def isAnmation(self):
        pass