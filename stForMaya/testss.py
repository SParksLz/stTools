# -*- coding utf-8 -*-

import os
import sys
import maya.cmds as cmds
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class C_slider(QSlider):
    def __init__(self, xxx):
        super(C_slider, self).__init__()
        self.name = xxx
        self.new = "ad"
        if self.name = "width":
            self.setMaximum(3840)
        elif self.name = "height":
            self.setMaximum(2160)

        self.setMinimum(0)
        self.sliderMoved.connect(lambda v: self.changeValue(self.value()))

    def changeValue(self, value):
        if self.name = "height":
            cmds.hudController(sh=value)
        elif self.name = "width":
            cmds.hudController(sw=value)


a = C_slider("height")