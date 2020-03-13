import os
import maya.cmds as cmds
import pymel.core as pmc
import getpass
import DeadlineInstance as di
def createJobInfo(outputDir, outputFile) :
    jobName = 'export alembic with maya standalone'
    userName = getpass.getuser()
    # jobStartFrame = str(startframe)
    # jobEndFrame = str(endframe)
    jobPlugin = 'MayaPython'
    Pool = 'liuz'
    jobInfo = {
        'Name':jobName,
        'UserName' : userName,
        'Plugin':jobPlugin,
        'Pool':Pool,
        'OutFile':outputFile,
        'OutDir':outputDir
    }
    return jobInfo

def createPluginInfo(targetobj, outputPath, startframe, endframe, mayaVersion, action, sceneFile) :
    pluginMayaVersion = mayaVersion
    pluginStartFrame = startframe
    pluginEndFrame = endframe
    pluginOutputPath = outputPath
    pluginTargetObj = targetobj
    pluginAction = action
    pluginSceneFile = sceneFile
    pluginInfo = {
        'Version':pluginMayaVersion,
        'Action':action,
        'StartFrame_test':pluginStartFrame,
        'EndFrame_test':pluginEndFrame,
        'Targetobject':pluginTargetObj,
        'SceneFile': pluginSceneFile,
        'Action':pluginAction,
        'OutputFilePath':pluginOutputPath
    }
    return pluginInfo




def submitAbcExport(mayaFile, targetobj, outputDir, fileName, startFrame, endFrame, version) :
    deadlineInstance = di.getDeadlineInstance()
    output_path = os.path.join(outputDir, fileName)
    outputDirList = [outputDir]
    outputFileList = [fileName]
    print outputDirList
    print outputFileList
    jobInfo = createJobInfo(outputDirList, outputFileList)
    pluginInfo = createPluginInfo(targetobj, output_path, int(startFrame), int(endFrame), version, 'alembic', mayaFile)
    deadlineInstance.Jobs.SubmitJob(jobInfo, pluginInfo)



def createRedshiftRenderJobInfo(outputDir, outputFile, startFrame, endFrame) :  
    userName = getpass.getuser()
    jobName = 'turntable rendering with redshift'
    jobPlugin = 'MayaBatch'
    Pool = 'liuz'
    framesInfo = {'Frames':'{0}-{1}'.format(startFrame, endFrame)}
    jobInfo = {}
    jobInfo['Name'] = jobName
    jobInfo['UserName'] = userName
    jobInfo['Plugin'] = jobPlugin
    jobInfo['Pool'] = Pool
    jobInfo['OutFile'] = [outputFile]
    jobInfo['OutDir'] = [outputDir]
    jobInfo['Frames'] = '{0}-{1}'.format(startFrame, endFrame)
    jobInfo['Props'] = framesInfo


    return jobInfo

def createRedshiftRenderPluginInfo(outputPath, outputFileName, startFrame, endFrame, renderer, mayaVersion, sceneFile, projectPath) :  
    PlugInfo = {}
    PlugInfo['Animation'] = '1'
    PlugInfo['ImageHeight'] = '1080'
    PlugInfo['ImageWidth'] = '1920'
    PlugInfo['Renderer'] = renderer
    PlugInfo['Version'] = mayaVersion
    PlugInfo['SceneFile'] = sceneFile
    PlugInfo['RedshiftVerbose'] = 2
    PlugInfo['OutputFilePath'] = outputPath
    PlugInfo['ProjectPath'] = projectPath

    return PlugInfo


def submitRedshiftTurntable(ttOutputFileDir, ttOutputFileName, startFrame, endFrame, projectPath, mayaVersion, sceneFile ) :  
    deadlineInstance = di.getDeadlineInstance()
    jobInfo = createRedshiftRenderJobInfo(ttOutputFileDir, ttOutputFileName, startFrame, endFrame)
    PlugInfo = createRedshiftRenderPluginInfo(ttOutputFileDir, ttOutputFileName, startFrame, endFrame, 'redshift', mayaVersion, sceneFile, projectPath)
    print jobInfo
    print PlugInfo
    deadlineInstance.Jobs.SubmitJob(jobInfo, PlugInfo)

def submithwplayblast(ttOutputFileDir, ttOutputFileName, startFrame, endFrame, projectPath, mayaVersion, sceneFile ) :  
    deadlineInstance = di.getDeadlineInstance()
    jobInfo = createRedshiftRenderJobInfo(ttOutputFileDir, ttOutputFileName, startFrame, endFrame)
    PlugInfo = createRedshiftRenderPluginInfo(ttOutputFileDir, ttOutputFileName, startFrame, endFrame, 'mayaHardware2', mayaVersion, sceneFile, projectPath)
    print jobInfo
    print PlugInfo
    deadlineInstance.Jobs.SubmitJob(jobInfo, PlugInfo)
