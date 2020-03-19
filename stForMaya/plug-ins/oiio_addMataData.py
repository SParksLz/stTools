import os
import maya.api.OpenMaya as om
import math
import OpenImageIO as oiio

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using Maya Python API 2.0.
    """
    pass

class addMetaData(om.MPxCommand) :

    cmdName = 'addMetaData'

    basePathFlag = '-bp'
    basePathFlagLong = '-basePath'
    mayaFileFlag = '-mf'
    mayaFileFlagLong = '-mayaFile'


    cameraFlag = '-c'
    cameraFlagLong = '-camera'
    currentFrame = '-cf'
    currentFrameLong = '-currentFrame'
    fileFlag = '-f'
    fileFlagLong = '-file'


    def __init__(self):
        super(addMetaData, self).__init__()

    @staticmethod
    def creator():
        return addMetaData()

    @staticmethod
    def createSyntax():
        syntax = om.MSyntax()
        syntax.setObjectType(om.MSyntax.kSelectionList)
        syntax.useSelectionAsDefault(True)
        syntax.addFlag(addMetaData.basePathFlag, addMetaData.basePathFlagLong, om.MSyntax.kString)
        syntax.addFlag(addMetaData.mayaFileFlag, addMetaData.mayaFileFlagLong, om.MSyntax.kString)
        syntax.addFlag(addMetaData.fileFlag, addMetaData.fileFlagLong, om.MSyntax.kString)
        syntax.addFlag(addMetaData.cameraFlag, addMetaData.cameraFlagLong, om.MSyntax.kString)
        syntax.addFlag(addMetaData.currentFrame, addMetaData.currentFrameLong, om.MSyntax.kTime)

        return syntax


    def doIt(self, args) :
        try:
            argdb = om.MArgDatabase(self.syntax(), args)
        except RuntimeError :
            om.MGlobal.displayError('Error while parsing arguments:\n#\t# If passing in list of nodes, also check that node names exist in scene.')

        if argdb.isFlagSet(addMetaData.basePathFlag) :
            mayaBaseDir = argdb.flagArgumentString(addMetaData.basePathFlag, 0)

        if argdb.isFlagSet(addMetaData.mayaFileFlag) :
            mayaFileName = argdb.flagArgumentString(addMetaData.mayaFileFlag, 0)


        if argdb.isFlagSet(addMetaData.cameraFlag) :
            name = argdb.flagArgumentString(addMetaData.cameraFlag, 0)
        else :
            om.MGlobal.displayError('cameraName is not set')

        if argdb.isFlagSet(addMetaData.currentFrame) :
            frameNumber = argdb.flagArgumentMTime(addMetaData.currentFrame, 0)
        else :
            om.MGlobal.displayError('current Frame is not specify')

        if argdb.isFlagSet(addMetaData.fileFlag) :
            filePath = argdb.flagArgumentString(addMetaData.fileFlag, 0)




        if name and frameNumber and filePath and mayaBaseDir and mayaFileName :
            currentCameraPosition = self.getWorldPosition(name, frameNumber)[0]
            prevCameraPosition = self.getWorldPosition(name, frameNumber-1)[0]
            currentCameraRotation = self.getWorldPosition(name, frameNumber)[1]


            currentSpeed = self.calculateSpeed(currentCameraPosition, prevCameraPosition)
            fullFileName = self.getFileName(mayaBaseDir, frameNumber, mayaFileName)
            om.MGlobal.displayInfo('image full path is {0}'.format(fullFileName))
            testVector = om.MVector(currentCameraRotation[0], currentCameraRotation[1], currentCameraRotation[2])
            testr = om.MEulerRotation(testVector, order=0)
            om.MGlobal.displayInfo('add metaData to image')
            self.addmetaData2EXR(fullFileName, currentSpeed, testr)




    def getFileName(self, basepath, currentFrame, fileName):
        padding = '4'
        num = currentFrame.value
        # om.MGlobal.displayInfo(num)
        pad = ("%%0%si" % padding) % int(num)
        imgFileName = '{0}.{1}.exr'.format(fileName, pad)

        fullPath = os.path.join(basepath, imgFileName)
        return fullPath




    def addmetaData2EXR(self, fileName, speed, rotation):
        currentMph = float(speed)
        currentTilt = round(math.degrees(rotation[0]), 1)
        currentPan = round(math.degrees(rotation[1]), 1)
        currentRoll = round(math.degrees(rotation[2]), 1)
        input_file = oiio.ImageInput.open(fileName)
        spec_file = input_file.spec()
        pixels = input_file.read_image()

        output = oiio.ImageOutput.create(fileName)
        spec_file.attribute('cameraSpeed', currentMph)
        spec_file.attribute('cameraTilt', currentTilt)
        spec_file.attribute('cameraPan', currentPan)
        spec_file.attribute('cameraRoll', currentRoll)
        output.open(fileName, spec_file)
        output.write_image(pixels)
        output.close()

    def calculateSpeed(self, currentPostion, prevPostion) :
        current_pos_x = currentPostion[0]
        current_pos_y = currentPostion[1]
        current_pos_z = currentPostion[2]

        prev_pos_x = prevPostion[0]
        prev_pos_y = prevPostion[1]
        prev_pos_z = prevPostion[2]

        current_move_x = current_pos_x - prev_pos_x
        current_move_y = current_pos_y - prev_pos_y
        current_move_z = current_pos_z - prev_pos_z

        move_length = math.sqrt((current_move_x) ** 2 + (current_move_y) ** 2 + (current_move_z) ** 2)
        current_speed = move_length * 25 / 60
        current_mph = round(current_speed/100*3.6*1.61, 1)

        return current_mph





    def getWorldPosition(self, camera, frame):

        ### get matrixPlug
        selectionList = om.MSelectionList()
        selectionList.add(camera)
        object_a = selectionList.getDependNode(0)
        fn_objectA = om.MFnDependencyNode(object_a)
        worldMatrixAttr = fn_objectA.attribute('worldMatrix')
        matrixPlug = om.MPlug(object_a, worldMatrixAttr)
        matrixPlug = matrixPlug.elementByLogicalIndex(0)

        ### get frame
        time = om.MTime(frame)
        FrameContext = om.MDGContext(time)

        matrixObject = matrixPlug.asMObject(FrameContext)
        worldMatrixData = om.MFnMatrixData(matrixObject)
        worldmatrix = worldMatrixData.matrix()

        mTransformMatrix = om.MTransformationMatrix(worldmatrix)
        worldRotation = mTransformMatrix.rotation(asQuaternion=False)
        worldPosition = mTransformMatrix.translation(om.MSpace.kWorld)
        data = [worldPosition, worldRotation]
        return data


def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    pluginFn.registerCommand(addMetaData.cmdName,
                             addMetaData.creator,
                             addMetaData.createSyntax)


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    pluginFn.deregisterCommand(addMetaData.cmdName)