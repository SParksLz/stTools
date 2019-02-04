# -*- coding: utf-8 -*-
import os
import sys

class file_control(object) :
    def __init__(self):

        #current
        self.current_dir = os.path.dirname(__file__)
        self.current_path = os.path.realpath(__file__)
        #parent
        self.parent_dir = "%s" %(os.path.sep).join(self.current_dir.split("%s" % (os.path.sep))[0:-1])
        self.Icon_dir = self.parent_dir+os.path.sep+"Icon"


    def getDirLst(self) :
        self.listDir = []
        for i in os.listdir(self.parent_dir) :
            self.listDir.append(self.parent_dir+os.path.sep+i)
        return self.listDir

    def getCurrentDir(self) :
        return self.current_dir

    def getCurrentPath(self) :
        return self.current_path

    def getParentDir(self) :
        return self.parent_dir

    def getIconDir(self) :
        return self.Icon_dir


