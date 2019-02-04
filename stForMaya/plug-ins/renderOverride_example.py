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


class ManipulatorSceneRender(omr.MUserRenderOperation):
    """Render Manipulator object on current selection position."""

    def __init__(self, name):
        # type: (Text) -> None
        super(ManipulatorSceneRender, self).__init__(name)
        self._initializeTemporalyVariables()

    def _initializeTemporalyVariables(self):
        # type: () -> None

        self.hiColor = om.MColor(om.MVector(1, 1, 0))

        self.xcolor = om.MColor(om.MVector(1, 0, 0))
        self.xmat = om.MMatrix((
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (1, 0, 0, 1)
        ))

        self.ycolor = om.MColor(om.MVector(0, 1, 0))
        self.ymat = om.MMatrix((
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 1, 0, 1)
        ))

        self.zcolor = om.MColor(om.MVector(0, 0, 1))
        self.zmat = om.MMatrix((
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 1)
        ))

        self.grayColor = om.MColor(om.MVector(0.3, 0.3, 0.3))

        self.coneRadius = 0.1
        self.coneHeight = 0.6
    # ------------------------------------------------------------------------

    def hasUIDrawables(self):
        # type: () -> bool
        return True

    def requiresLightData(self):
        # type: () -> bool
        return False

    def execute(self, context):
        # type: (omr.MDrawContext) -> None
        pass

    def addUIDrawables(self, drawManager, frameContext):
        # type: (omui.MUIDrawManager, omr.MFrameContext) -> bool

        if (not omani.MAnimControl.isPlaying() and not omani.MAnimControl.isScrubbing()):
            return False

        target = self._getTargetDagPath()
        if not target:
            return True

        tool, axis = self._getToolContext()
        if not tool:
            return True

        self._draw(drawManager, target, tool, axis)
        return True

    # ------------------------------------------------------------------------

    def _getTargetDagPath(self):
        # type: () -> om.MDagPath
        """Return current selection object's dagPath."""

        sel = om.MGlobal.getActiveSelectionList()
        len = sel.length()
        if 0 == len:
            return

        target = sel.getComponent(len - 1)[0]
        return target

    def _getToolContext(self):
        # type: () -> Tuple[Text]
        """Return current current tool context and activeHandle as Text.
        context: "move" or "rotate"
        activeAxis: int [0: x, 1: y, 2:z, 3:not restricted]
        """

        ctx = mel.eval("currentCtx;")  # type: Text
        if "move" in ctx.lower():
            activeHandle = mel.eval("manipMoveContext -q -currentActiveHandle Move;")
            return "move", activeHandle

        elif "rotate" in ctx.lower():
            activeHandle = mel.eval("manipRotateContext -q -currentActiveHandle Rotate;")
            return "rotate", activeHandle

        return "", None

    # ------------------------------------------------------------------------

    def _draw(self, manager, dagPath, tool, activeAxis):
        # type: (omui.MUIDrawManager, om.MDagPath, Text, int) -> None
        """Draw manipulator shape using MUIDrawManager.
        Depending the tool context, draw arrow gizmo or spherical gizmo.
        """

        worldMat = dagPath.inclusiveMatrix().homogenize()
        rotMat = om.MMatrix(worldMat)
        rotMat.setElement(3, 0, 0.0)
        rotMat.setElement(3, 1, 0.0)
        rotMat.setElement(3, 2, 0.0)

        # start point position
        posx = worldMat.getElement(3, 0)
        posy = worldMat.getElement(3, 1)
        posz = worldMat.getElement(3, 2)
        point = om.MPoint(posx, posy, posz)

        xcol = self.hiColor if activeAxis == 0 else self.xcolor
        ycol = self.hiColor if activeAxis == 1 else self.ycolor
        zcol = self.hiColor if activeAxis == 2 else self.zcolor

        manager.beginDrawInXray()

        if "move" == tool:
            self._drawArrow(manager, point, worldMat, rotMat, self.xmat, xcol)
            self._drawArrow(manager, point, worldMat, rotMat, self.ymat, ycol)
            self._drawArrow(manager, point, worldMat, rotMat, self.zmat, zcol)

        elif "rotate" == tool:
            self._drawCircle(manager, point, worldMat, rotMat, self.xmat, xcol)
            self._drawCircle(manager, point, worldMat, rotMat, self.ymat, ycol)
            self._drawCircle(manager, point, worldMat, rotMat, self.zmat, zcol)

        manager.endDrawInXray()

    def _drawArrow(self, manager, basePoint, worldMat, rotMat, distanceMat, color):
        # type: (omui.MUIDrawManager, om.MPoint, om.MMatrix, om.MMatrix, om.MMatrix, om.MColor) -> None

        manager.setColor(color)

        camZoom = self._zoomRatio(basePoint)

        # draw line
        endMat = worldMat + (distanceMat * camZoom * rotMat)
        posx = endMat.getElement(3, 0)
        posy = endMat.getElement(3, 1)
        posz = endMat.getElement(3, 2)
        endPoint = om.MPoint(posx, posy, posz)

        manager.line(basePoint, endPoint)

        # draw cone(base, direction, radius, height, filled=False) -> self
        direction = om.MVector()
        direction.x = posx - basePoint.x
        direction.y = posy - basePoint.y
        direction.z = posz - basePoint.z
        w = self.coneRadius * camZoom
        h = self.coneHeight * camZoom
        manager.cone(endPoint, direction, w, h, True)

    def _drawCircle(self, manager, basePoint, worldMat, rotMat, distanceMat, color):
        # type: (omui.MUIDrawManager, om.MPoint, om.MMatrix, om.MMatrix, om.MMatrix, om.MColor) -> None
        # TODO(implement later): draw gray color half side not facing camera

        camZoom = self._zoomRatio(basePoint)

        endMat = worldMat + (distanceMat * camZoom * rotMat)
        posx = endMat.getElement(3, 0)
        posy = endMat.getElement(3, 1)
        posz = endMat.getElement(3, 2)
        # startVec = om.MVector(posx * -1, posy, posz)
        # endVec = om.MVector(posx, posy, posz)

        direction = om.MVector()
        direction.x = basePoint.x - posx
        direction.y = basePoint.y - posy
        direction.z = basePoint.z - posz

        manager.setColor(color)
        manager.circle(basePoint, direction, 0.84 * camZoom, False)

        # color arc
        # arc(center, start, end, normal, radius, filled=False) -> self
        # arc2d(center, start, end, radius, filled=False) -> self
        # gray circle
        # manager.setColor(self.grayColor)
        # manager.arc(basePoint, startVec, endVec, direction, 0.84 * camZoom, False)

    def _zoomRatio(self, basePoint):
        # type: (om.MPoint) -> float
        """Calculate zoom factor as distance from the current view's camera position."""
        # FIXME: all views share this value from current one.

        # camera distance
        cameraPath = omui.M3dView.active3dView().getCamera()
        camNode = om.MFnDependencyNode(cameraPath.node())
        isOrtho = camNode.findPlug("orthographic", False)

        camMat = cameraPath.inclusiveMatrix().homogenize()
        camPos = om.MPoint(
            camMat.getElement(3, 0),
            camMat.getElement(3, 1),
            camMat.getElement(3, 2),
        )

        if isOrtho.asBool():
            orthoWidth = camNode.findPlug("orthographicWidth", False).asFloat()
            return math.ldexp(orthoWidth, 3) * 0.01
        else:
            return basePoint.distanceTo(camPos) * 0.1

class hud_test(omr.MHUDRender) :
    def __init__(self):
        super(hud_test, self).__init__()



    def hasUIDrawables(self) :
        return True


    def addUIDrawables(self, drawManager2D, frameContext) :
        drawManager2D.beginDrawable()
        drawManager2D.setColor(om.MColor((0.5, 0.2, 0.6)))
        drawManager2D.setFontSize( omr.MUIDrawManager.kSmallFontSize )
        window_size = frameContext.getViewportDimensions()
        print window_size
        drawManager2D.text2d(om.MPoint(window_size[2]/3, window_size[3]/4), "Hello world!", omr.MUIDrawManager.kCenter )


        drawManager2D.line2d(om.MPoint(0, window_size[3]/2-540/6), om.MPoint(window_size[2], window_size[3]/2-540/6))
        drawManager2D.line2d(om.MPoint(0, window_size[3]/2+540/6), om.MPoint(window_size[2], window_size[3]/2+540/6))
        drawManager2D.line2d(om.MPoint(window_size[2]/2-960/6, 0), om.MPoint(window_size[2]/2-960/6, window_size[3]))
        drawManager2D.line2d(om.MPoint(window_size[2]/2+960/6, 0), om.MPoint(window_size[2]/2+960/6, window_size[3]))
        # drawManager2D.line2D(om.Mpoint(0, window_size[3]), om.MPoint())
        drawManager2D.endDrawable()




class DrawManipulatorOverride(omr.MRenderOverride):
    """Pass."""

    def __init__(self, name):
        # type: (Text) -> None
        self.operatioIndex = 0
        self.operations = [
            omr.MSceneRender("scene"),
            ManipulatorSceneRender("manipulatorRender"),
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
    om.MFnPlugin(mobj, __author__, __version__, 'Any')

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