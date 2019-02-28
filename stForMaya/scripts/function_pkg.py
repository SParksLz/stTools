# -*- coding utf-8 -*-

import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *


def mayaToQObject(mayaUI) :
    ptr = omui.MQtUtil.findControl( mayaUI )
    if ptr is None :
        ptr = omui.MQtUtil.findWindow( mayaUI )
    if ptr is None :
        ptr = omui.MQtUtil.findLayout( mayaUI )
    if ptr is None :
        ptr = omui.MQtUtil.findControl( mayaUI )
    if ptr is not None :
        return wrapInstance(long(ptr), QObject)