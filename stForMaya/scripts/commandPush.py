import os
import sys

import maya.cmds as cmds
import pymel.core as pmc
import maya.api.OpenMaya as om
from PySide2.QtWidgets import *
from PySide2.QtCore import *




class cmdMaker(object) :
    def __init__(self, publishPath, cameraName, presets, renderMode, imagePath):
        self.pubFile = publishPath
        self.pubName = os.path.basename(publishPath)
        self.mayaFile = pmc.sceneName()
        self.cameraName = cameraName
        self.presets = presets
        self.localPath = __file__
        self.localDir = os.path.dirname(self.localPath)
        self.baseCmd = "Render -r hw2 "
        self.renderMode = renderMode
        self.imagePath = imagePath
        if self.presets == "hd1080" :   
            self.height = 1080
            self.width = 1920
        elif self.presets == "hd720" :  
            self.height = 720
            self.width = 1280

        else :  
            self.height = 720
            self.width = 1280
        if renderMode == "previz" :  
            self.templatePath = os.path.join(self.localDir, 'settingTemplate_previz.json')
        elif renderMode == "default" :  
            self.templatePath = os.path.join(self.localDir, 'settingTemplate_default.json')

        else :  
            self.templatePath = os.path.join(self.localDir, 'settingTemplate_default.json')


        self.mayaFileDir = str(self.mayaFile.dirname())
        self.mayaFilePath = str(self.mayaFile)
        self.mayaFileName = str(self.mayaFile.basename())

        self.startFrame = pmc.playbackOptions(q=1, min=1)
        self.endFrame = pmc.playbackOptions(q=1, max=1)




        # self.height = height
        # self.width = width



        # print "-"*20
        # print self.localPath
        print self.templatePath

    # def getDestPath(self) :
    #     # if os.path.exists(self.pubFile) :
    #     #     parentPath = os.path.abspath(os.path.join(self.pubFile, "../../.."))
    #     # else :
    #     #     parentPath = None
    #     parentPath = os.path.abspath(os.path.join(self.pubFile, "../../.."))

    #     print parentPath
    #     if parentPath is not None and os.path.basename(parentPath) == "SHARED" :
    #         newDir = os.path.join(parentPath, "IMG/anim/{0}".format(self.pubName.split(".")[0]))
    #     else :
    #         newDir = None

    #     return newDir

    def buildCmd(self):
        render = "hw2"
        # outputDir = self.getDestPath()
        presetPath = self.templatePath
        camera = self.cameraName
        startFrame = int(self.startFrame)
        endFrame = int(self.endFrame)
        publishedFile = self.pubFile
        imageDesPath = self.imagePath
        fileName = self.mayaFile.basename().split('.')[0]

        if self.renderMode == "default" :
            fullCmd = "Render -r {0} -rd {1} -preRender 'colorManagementPrefs -e -ote 1' -postFrame 'python \"import os;import maya.cmds as cmds; cmds.loadPlugin(\\\"oiio_addMataData\\\");cmds.addMetaData(mf=\\\"{2}\\\", bp=\\\"{1}\\\",c=\\\"{3}\\\", cf=cmds.currentTime(q=1), f=\\\"hello wrold!\\\")\"' -cam {3} -x {4} -y {5} -percentRes 100.00 -rsp {6} -s {7} -e {8} {9}".format(render, imageDesPath, fileName, camera, self.width, self.height, presetPath, startFrame, endFrame, publishedFile)
        elif self.renderMode == "previz" :
            fullCmd = "Render -r {0} -rd {1} -preRender 'colorManagementPrefs -e -ote 1' -cam {2} -x {3} -y {4} -percentRes 100.00 -s {5} -e {6} {7}".format(render, imageDesPath, camera, self.height, self.width, startFrame, endFrame, publishedFile)
        else :
            fullCmd = "Render -r {0} -rd {1} -preRender 'colorManagementPrefs -e -ote 1' -cam {2} -x {3} -y {4} -percentRes 100.00 -rsp {5} -s {6} -e {7} {8}".format(render, imageDesPath, camera, self.height, self.width, presetPath, startFrame, endFrame, publishedFile)

        return fullCmd



    # def printCommand(self):
    #     destDir = self.getDestPath()
    #     if destDir is not None  :
    #         if os.path.exists(destDir) :
    #             pass
    #         else :
    #             os.makedirs(destDir)





'''
preset     : "hd1080", "hd720"
renderMode :  "previz", "default"
'''
def submitCommand(publishPath, cameraName, presets, renderMode, imagePath) :
    solver = cmdMaker(publishPath, cameraName, presets, renderMode, imagePath)
    fullCommand = solver.buildCmd()
    return fullCommand





def submitDebug() :
    publishPath = str(pmc.sceneName())
    projectPath = cmds.workspace(q=1, fullName=1)
    imagePath = os.path.join(projectPath, "images")
    presets_d = "hd1080"
    renderMode_d = "default"
    testWindow = QWidget()
    base_layout = QVBoxLayout()
    test_comboBox = QComboBox()
    all_camera = cmds.ls(cameras=True)
    test_comboBox.addItems(all_camera)

    presets_comBox = QComboBox()
    presets_comBox.addItems(["hd1080", "hd720"])

    mode_comBox = QComboBox()
    mode_comBox.addItems(["default", "previz"])

    test_button = QPushButton("generate")
    base_layout.addWidget(test_comboBox)
    base_layout.addWidget(presets_comBox)
    base_layout.addWidget(mode_comBox)
    base_layout.addWidget(test_button)
    testWindow.setLayout(base_layout)


    test_button.clicked.connect(lambda : submitAA(publishPath, test_comboBox.currentText(), presets_comBox.currentText(), mode_comBox.currentText(), imagePath))

    return testWindow



def submitAA(publishPath, cameraName, presets_d, renderMode_d, imagePath):
    fullCommand = submitCommand(publishPath, cameraName, presets_d, renderMode_d, imagePath)
    om.MGlobal.displayInfo("{0}".format(fullCommand))
