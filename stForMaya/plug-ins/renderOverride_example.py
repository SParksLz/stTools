# -*- coding: utf-8 -*-
# @Author: dirty
# @Date:   2019-02-04 01:41:25
# @Last Modified by:   dirty
# @Last Modified time: 2019-02-04 06:12:11
"""Custom Render Override for drawnig Manipulator even during playback."""
###############################################################################
import sys
import math


import pymel.core as pmc

import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaAnim as omani
import maya.api.OpenMayaRender as omr
import maya.mel as mel



if False:
    # For mypy type annotation
    from typing import (  # NOQA
        Dict,
        List,
        Tuple,
        Pattern,
        Callable,
        Any,
        Text,
        Union
    )

###############################################################################

maya_useNewAPI = True
renderOverrideInstance = None  # type: DrawManipulatorOverride



###############################################################################




class hud_test(omr.MHUDRender) :
    def __init__(self):
        super(hud_test, self).__init__()



    def hasUIDrawables(self) :
        return True


    def addUIDrawables(self, drawManager2D, frameContext) :

        defaultResolution = pmc.PyNode("defaultResolution")
        render_height = defaultResolution.getAttr("height")
        rebder_width = defaultResolution.getAttr("width")

        drawManager2D.beginDrawable()
        drawManager2D.setColor(om.MColor((0.5, 0.2, 0.6)))
        drawManager2D.setFontSize( omr.MUIDrawManager.kSmallFontSize )
        window_size = frameContext.getViewportDimensions()
        print window_size
        drawManager2D.text2d(om.MPoint(window_size[2]/3, window_size[3]/4), "波风水门", omr.MUIDrawManager.kCenter )


        drawManager2D.line2d(om.MPoint(0, window_size[3]/2-render_height/6), om.MPoint(window_size[2], window_size[3]/2-render_height/6))
        drawManager2D.line2d(om.MPoint(0, window_size[3]/2+render_height/6), om.MPoint(window_size[2], window_size[3]/2+render_height/6))
        drawManager2D.line2d(om.MPoint(window_size[2]/2-rebder_width/6, 0), om.MPoint(window_size[2]/2-rebder_width/6, window_size[3]))
        drawManager2D.line2d(om.MPoint(window_size[2]/2+rebder_width/6, 0), om.MPoint(window_size[2]/2+rebder_width/6, window_size[3]))
        # drawManager2D.line2D(om.Mpoint(0, window_size[3]), om.MPoint())
        drawManager2D.endDrawable()




class DrawManipulatorOverride(omr.MRenderOverride):
    """Pass."""

    def __init__(self, name):
        # type: (Text) -> None
        self.operationIndex = 0
        self.operations = [
            omr.MSceneRender("scene"),
            hud_test(),
            omr.MPresentTarget("present")
        ]

        self.operations[0].clearOperation().setOverridesColors(False)
        super(DrawManipulatorOverride, self).__init__(name)

    def uiName(self):
        # type: () -> Text
        return "Manipulator Drawer"

    def setup(self, destination):
        # type: (Text) -> None
        super(DrawManipulatorOverride, self).setup(destination)

    def cleanup(self):
        # type: () -> None
        super(DrawManipulatorOverride, self).cleanup()

    def supportedDrawAPIs(self):
        # type: () -> int
        return omr.MRenderer.kAllDevices

    def startOperationIterator(self):
        # type: () -> bool
        self.operationIndex = 0
        return True

    def renderOperation(self):
        # type: () -> omr.MRenderOperation
        return self.operations[self.operationIndex]

    def nextRenderOperation(self):
        # type: () -> bool
        self.operationIndex += 1
        return self.operationIndex < len(self.operations)






def initializePlugin(mobj):
    om.MFnPlugin(mobj, "liuzhen", "2017", 'Any')

    try:
        global renderOverrideInstance
        renderOverrideInstance = DrawManipulatorOverride("DrawManipulatorDuringPlayback")
        omr.MRenderer.registerOverride(renderOverrideInstance)

    except Exception:
        sys.stderr.write("registerOverride\n")
        om.MGlobal.displayError("registerOverride")
        raise


def uninitializePlugin(mobj):
    # plugin = om.MFnPlugin(mobj)
    # print(plugin)

    try:
        global renderOverrideInstance
        if renderOverrideInstance is not None:
            omr.MRenderer.deregisterOverride(renderOverrideInstance)
            renderOverrideInstance = None

    except Exception:
        sys.stderr.write("deregisterOverride\n")
        om.MGlobal.displayError("deregisterOverride")
        raise