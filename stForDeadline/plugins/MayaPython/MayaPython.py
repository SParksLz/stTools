import os
import sys
import re


from System.IO import *
from System.Text.RegularExpressions import *

from Deadline.Plugins import *
from Deadline.Scripting import *

def GetDeadlinePlugin():
    return PythonPlugin()

def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()

class PythonPlugin (DeadlinePlugin):
    
    def __init__( self ):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
    
    def Cleanup(self):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback
        
        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback
    
    def InitializeProcess(self):
        self.PluginType = PluginType.Simple
        self.StdoutHandling = True
        # self.standaloneAction = self.GetPluginInfoEntryWithDefault('Action', '')

        
        # self.SingleFramesOnly = self.GetBooleanPluginInfoEntryWithDefault( "SingleFramesOnly", False )
        # self.LogInfo( "Single Frames Only: %s" % self.SingleFramesOnly )

        self.AddStdoutHandlerCallback( ".*Progress: (\d+)%.*" ).HandleCallback += self.HandleProgress

        # localPythonHome = '/usr/lib64/python2.7'
        # localPythonPath = '/usr/lib64/python2.7/site-packages'
        # pythonPath = self.GetEnvironmentVariable( "PYTHONPATH" ).strip()
        # addingPaths = self.GetConfigEntryWithDefault( "PythonSearchPaths", "" ).strip()
        
        # if addingPaths != "":
        #     addingPaths.replace( ';', os.pathsep )
            
        #     if pythonPath != "":
        #         pythonPath = pythonPath + os.pathsep + addingPaths
        #     else:
        #         pythonPath = addingPaths
        # print "Setting PYTHONPATH to: " + localPythonHome 
        # # self.LogInfo( "Setting PYTHONPATH to: " + localPythonHome )
        # self.SetEnvironmentVariable( "PYTHONHOME", localPythonHome )
        # self.SetEnvironmentVariable( "PYTHONPATH", localPythonPath)
    
    def RenderExecutable( self ):
        version = self.GetPluginInfoEntry( "Version" )
        version = version.replace(".", "_")
        exeList = self.GetConfigEntry( "MayaPythonExecutable_" + version)
        exe = FileUtils.SearchFileList( exeList )
        if exe == "":
            self.FailRender( "Python " + version + " executable was not found in the semicolon separated list \"" + exeList + "\". The path to the render executable can be configured from the Plugin Configuration in the Deadline Monitor." )
        return exe
    
    def RenderArgument( self ):
        action = self.GetPluginInfoEntryWithDefault('Action', '')
        if action :  
            if action == 'alembic' :  
                scriptFile = RepositoryUtils.CheckPathMapping('/apps/shared/ddp/ddpmayastandalone/0.0.1/ddpmayastandalone/MayapyExportAbc.py')

            elif action == 'rsproxy' :  
                scriptFile = RepositoryUtils.CheckPathMapping('/apps/shared/ddp/ddpmayastandalone/0.0.1/ddpmayastandalone/PythonMayaExportRsProxy')
        outputPath = self.GetPluginInfoEntryWithDefault('OutputFilePath', '')
        targetObjects = str(self.GetPluginInfoEntryWithDefault('Targetobject', ''))
        print type(targetObjects)
        print "#########################3"
        print targetObjects
        startFrame = self.GetIntegerPluginInfoEntryWithDefault('StartFrame_test', 0)
        endFrame = self.GetIntegerPluginInfoEntryWithDefault('EndFrame_test', 0)
        sceneFile = self.GetPluginInfoEntryWithDefault('SceneFile', '')

        scriptArg = '{0}'.format(scriptFile)
        outputArg = ' -alembicFile {0}'.format(outputPath)
        fileArg = ' -mayaFile {0}'.format(sceneFile)
        frameRangeArg = ' -frameRange {0} {1}'.format(startFrame, endFrame)
        rootArgument = ' -root'
        if isinstance(targetObjects, str) :
            rootArgument += ' {0}'.format(targetObjects)
            print rootArgument
        elif isinstance(targetObjects, list) :
            for targetObject in targetObjects :
                rootArgument += ' {0}'.format(targetObject)
                print rootArgument

        frameRangeArg = ' -frameRange {0} {1}'.format(startFrame, endFrame)
        renderableArg = ' -renderableOnly'
        facesetsArg = ' -writeFaceSets'
        uvArg = ' -uvWrite'
        worldSpace = ' -worldSpace'
        writeVisibility = ' -writeVisibility'
        dataFormatArg = ' -dataFormat Ogawa'


        optionArgs = scriptArg+outputArg+fileArg+frameRangeArg+rootArgument+frameRangeArg+renderableArg+facesetsArg+uvArg+worldSpace+writeVisibility+dataFormatArg


        # scriptFile = self.GetPluginInfoEntryWithDefault( "ScriptFile", self.GetDataFilename() )
        # scriptFile = RepositoryUtils.CheckPathMapping( scriptFile )
        
        # arguments = self.GetPluginInfoEntryWithDefault( "Arguments", "" )
        # arguments = RepositoryUtils.CheckPathMapping( arguments )

        # arguments = re.sub( r"<(?i)STARTFRAME>", str( self.GetStartFrame() ), arguments )
        # arguments = re.sub( r"<(?i)ENDFRAME>", str( self.GetEndFrame() ), arguments )
        # arguments = re.sub( r"<(?i)QUOTE>", "\"", arguments)

        # arguments = self.ReplacePaddedFrame( arguments, "<(?i)STARTFRAME%([0-9]+)>", self.GetStartFrame() )
        # arguments = self.ReplacePaddedFrame( arguments, "<(?i)ENDFRAME%([0-9]+)>", self.GetEndFrame() )

        # count = 0
        # for filename in self.GetAuxiliaryFilenames():
        #     localAuxFile = Path.Combine( self.GetJobsDataDirectory(), filename )
        #     arguments = re.sub( r"<(?i)AUXFILE" + str( count ) + r">", localAuxFile.replace( "\\", "/" ), arguments )
        #     count += 1

        # if SystemUtils.IsRunningOnWindows():
        #     scriptFile = scriptFile.replace( "/", "\\" )
        # else:
        #     scriptFile = scriptFile.replace( "\\", "/" )

        # return "-u \"" + scriptFile + "\" " + arguments
        # return "\"" + optionArgs + "\" "
        return optionArgs



    def ReplacePaddedFrame( self, arguments, pattern, frame ):
        frameRegex = Regex( pattern )
        while True:
            frameMatch = frameRegex.Match( arguments )
            if frameMatch.Success:
                paddingSize = int( frameMatch.Groups[ 1 ].Value )
                if paddingSize > 0:
                    padding = StringUtils.ToZeroPaddedString( frame, paddingSize, False )
                else:
                    padding = str(frame)
                arguments = arguments.replace( frameMatch.Groups[ 0 ].Value, padding )
            else:
                break
        
        return arguments

    def HandleProgress( self ):
        progress = float( self.GetRegexMatch(1) )
        self.SetProgress( progress )
