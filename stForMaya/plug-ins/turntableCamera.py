import os
import sys
import math
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


def maya_useNewAPI() :
    pass

class turtableCameraCmd(om.MPxCommand) :
    cmdName = 'turntableCamera'
    geometryFlag = '-tg'
    geometryFlagLong = '-targetGeo'
    withBoundingBoxFlag = '-wbb'
    withBoundingBoxLong = '-withboundingbox'
    withObjectRotatePivotFlag = '-wrp'
    withObjectRotatePivotLong = '-withrotatepivot'


    def __init__(self):
        super(turtableCameraCmd, self).__init__()


    @staticmethod
    def creator() :
        return turtableCameraCmd()

    @staticmethod
    def createSyntax():
        syntax = om.MSyntax()
        syntax.setObjectType(om.MSyntax.kSelectionList)
        syntax.useSelectionAsDefault(True)
        syntax.addFlag(turtableCameraCmd.geometryFlag,
                       turtableCameraCmd.geometryFlagLong,
                       om.MSyntax.kString)

        syntax.addFlag(turtableCameraCmd.withBoundingBoxFlag,
                       turtableCameraCmd.withBoundingBoxLong,
                       om.MSyntax.kBoolean)
        syntax.addFlag(turtableCameraCmd.withObjectRotatePivotFlag,
                       turtableCameraCmd.withObjectRotatePivotLong,
                       om.MSyntax.kBoolean)

        return syntax


    def doIt(self, args):
        try:
            argdb = om.MArgDatabase(self.syntax(), args)
        except RuntimeError :
            om.MGlobal.displayError('Error while parsing arguments:\n#\t# If passing in list of nodes, also check that node names exist in scene.')

        if argdb.isFlagSet(turtableCameraCmd.geometryFlag) :
            turtable_target = argdb.flagArgumentString(turtableCameraCmd.geometryFlag, 0)

        if argdb.isFlagSet(turtableCameraCmd.withBoundingBoxFlag) and argdb.isFlagSet(turtableCameraCmd.withObjectRotatePivotFlag):
            raise ValueError('bb and rotate pivot flag can not existst in the same time!')

        if argdb.isFlagSet(turtableCameraCmd.withBoundingBoxFlag) :
            use_boundingBox = argdb.flagArgumentBool(turtableCameraCmd.withBoundingBoxFlag, 0)
        if argdb.isFlagSet(turtableCameraCmd.withObjectRotatePivotFlag) :
            use_rotatepivot = argdb.flagArgumentBool(turtableCameraCmd.withObjectRotatePivotFlag, 0)


        if turtable_target :
            tt_geoBoundingBox = self.getGeoBoundingandSetKey(turtable_target)

            if use_boundingBox :
                geoBoundingBox_center = tt_geoBoundingBox.center
                centerX = geoBoundingBox_center.x
                centerY = geoBoundingBox_center.y
                centerZ = geoBoundingBox_center.z
            elif use_rotatepivot :
                geoBoundingBox_center = self.getObjectCenter(turtable_target)
                centerX = geoBoundingBox_center.x
                centerY = geoBoundingBox_center.y
                centerZ = geoBoundingBox_center.z
            geoHeight = tt_geoBoundingBox.height
            geoWidth = tt_geoBoundingBox.width
            geoDepth = tt_geoBoundingBox.depth
            groupObject = self.buildGroup([centerX, centerY, centerZ], geoHeight)
            groupFn = om.MFnDagNode(groupObject)
            self.addExtraAttr(groupFn)
            currentCamFn, currentCamShapeFn = self.createCameraandReturnIt(groupObject)
            horizontalFilmAperture = currentCamShapeFn.findPlug('horizontalFilmAperture', False).asFloat()*2.54+5.0
            verticalFilmAperture = currentCamShapeFn.findPlug('verticalFilmAperture', False).asFloat()*2.54+0.7
            focalLength = currentCamShapeFn.findPlug('focalLength', False).asFloat()


            main_ref = geoHeight
            mainAperture = verticalFilmAperture

            if geoWidth < geoDepth :
                geoWidth = geoDepth

            if main_ref < geoWidth :
                main_ref = geoWidth
                mainAperture = horizontalFilmAperture



            print "{0}".format(focalLength/10)
            print "{0}    geowidth : {1}".format(main_ref, geoWidth/2)

            cameraDistance = focalLength/10*main_ref/2+main_ref/10*2/mainAperture+main_ref/2
            print "camera distance :  {0}".format(cameraDistance)
            camTranslateZ = currentCamFn.findPlug('translateZ', False)
            camTranslateZ.setFloat(cameraDistance)

            cc_translateX = currentCamFn.findPlug('translateX', False)
            cc_translateX.isLocked = True
            cc_translateY = currentCamFn.findPlug('translateY', False )
            cc_translateY.isLocked=True
            cc_translateZ = currentCamFn.findPlug('translateZ', False)
            cc_translateZ.isLocked=True
            cc_rotateX = currentCamFn.findPlug('rotateX', False)
            cc_rotateX.isLocked=True
            cc_rotateY = currentCamFn.findPlug('rotateY', False)
            cc_rotateY.isLocked=True
            cc_rotateZ = currentCamFn.findPlug('rotateZ', False)
            cc_rotateZ.isLocked=True

            self.setResult(groupFn.name())




    def buildGroup(self, center, height):
        transFn = om.MFnTransform()
        groupNode = transFn.create()
        groupFn = om.MFnDagNode(groupNode)
        translateX = groupFn.findPlug('translateX', False)
        translateY = groupFn.findPlug('translateY', False)
        translateZ = groupFn.findPlug('translateZ', False)
        rotateY = groupFn.findPlug('rotateY', False)
        # translateX.setFloat(center[0])
        translateY.setFloat(height/2)
        # translateZ.setFloat(center[2])

        animCureFn = oma.MFnAnimCurve()
        rotateYCurve = animCureFn.create(rotateY, animCurveType=0)
        rotateYFn = oma.MFnAnimCurve(rotateYCurve)
        self.addExtraAttr(rotateYFn)
        st_plug_obj = rotateYFn.findPlug("shader_type", False)
        st_plug_obj.setString('turntableShaderBall')


        twice_startTime = om.MTime(151.0, unit = 7)
        twice_endTime = om.MTime(200.0, unit=7)

        startAngle = om.MAngle(0.0, 2)
        endAngle = om.MAngle(-360.0, 2)
        rotateYFn.addKeys([twice_startTime, twice_endTime],
                          [startAngle.asRadians(),endAngle.asRadians()],
                          tangentInType=2,
                          tangentOutType=2)

        return groupNode


    def createCameraandReturnIt(self, parent):
        cameraFn = om.MFnCamera()
        cameraNode = cameraFn.create(parent)
        cameraDagFn = om.MFnDagNode(cameraNode)
        cameraDagPath = cameraDagFn.getPath()
        cameraShapeDagPath = cameraDagPath.extendToShape()
        cameraShapeDagFn = om.MFnDagNode(cameraShapeDagPath)
        lensPlug = cameraShapeDagFn.findPlug('focalLength', False)
        lensPlug.setFloat(60.0)


        return cameraDagFn, cameraShapeDagFn

    def getGeoBoundingandSetKey(self, geo):
        if not geo :
            raise ValueError('Geo flag can not be null')

        selectionList = om.MSelectionList()
        try :
            selectionList.add(geo)
        except RuntimeError :
            om.MGlobal.displayError('Object {0} does not exist '.format(geo))
            raise ValueError('Object {0} does not exist '.format(geo))
        geoDagPath = selectionList.getDagPath(0)
        selectionList.clear()
        geoFn = om.MFnTransform(geoDagPath)
        rotateY_plug = geoFn.findPlug('rotateY', False)
        geoBoundingBox = geoFn.boundingBox

        rotateY_connections_num = rotateY_plug.isConnected
        if rotateY_connections_num :
            om.MGlobal.displayError('can not connect to {0}.{1} because is has another connections'.format(geoFn.name(), rotateY_plug.name()))
            raise RuntimeError
        else :
            animCurve = oma.MFnAnimCurve()



            ac_object = animCurve.create(rotateY_plug, animCurveType=0)
            rotateYFn = oma.MFnAnimCurve(ac_object)
            self.addExtraAttr(rotateYFn)
            st_plug = animCurve.findPlug("shader_type", False)
            st_plug.setString('turntableShaderBall')
            startTime = om.MTime(0.0, unit=7)
            endTime = om.MTime(100.0, unit=7)
            startAngle = om.MAngle(0.0, 2)
            endAngle = om.MAngle(360.0, 2)
            rotateYFn.addKeys([startTime, endTime],
                              [startAngle.asRadians(),endAngle.asRadians()],
                              tangentInType=2,
                              tangentOutType=2)


        return geoBoundingBox


    def getObjectCenter(self, geo):
        geoSelectionList = om.MSelectionList()
        geoSelectionList.add(geo)
        geoDagPath = om.MDagPath(geo)
        geoTransFn = om.MFnTransform(geoDagPath)
        geoCenter = geoTransFn.rotatePivot(om.MSpace.kWorld)
        return geoCenter


    def setNodeAttr(self, nodeFn, attr, value):
        attrPlug = nodeFn.findPlug(attr, False)
        if isinstance(value, int) :
            attrPlug.setInt(value)

        elif isinstance(value, float) :
            attrPlug.setFloat(value)

        elif isinstance(value, bool) :
            attrPlug.setBool(value)


    def addExtraAttr(self, node) :
        fAttr = om.MFnTypedAttribute()
        turntableAttr = fAttr.create("shader_type", 'st', om.MFnData.kString)
        fAttr.storable = True
        fAttr.writable = True
        fAttr.readable = True
        node.addAttribute(turntableAttr)
        attr_plug = node.findPlug('shader_type', False)
        attr_plug.setString('turntableShaderBall')


def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    pluginFn.registerCommand(turtableCameraCmd.cmdName,
                             turtableCameraCmd.creator,
                             turtableCameraCmd.createSyntax)


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    pluginFn.deregisterCommand(turtableCameraCmd.cmdName)