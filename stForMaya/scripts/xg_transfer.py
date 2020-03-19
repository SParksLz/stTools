import os
import sys
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pmc
import maya.api.OpenMaya as om
from pprint import pprint
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import platform



def baseConfig() :
    config_dir = {}
    allsdNodes = cmds.xgmSplineQuery(listSplineDescriptions=True)
    tmp_dir = {}
    for sd in allsdNodes :
        sdnode = sd
        xg_base = cmds.ls(cmds.listHistory(sd), type="xgmSplineBase")[0]
        xg_mesh = cmds.listConnections("{0}.boundMesh".format(xg_base))[0]
        tmp_dir["base"] = xg_base
        tmp_dir["mesh"] = xg_mesh
        tmp_dir["name"] = sd
        tmp_dir.setdefault("sd", []).append(sd)
        config_dir.setdefault(tmp_dir["mesh"], []).append(tmp_dir["name"])

    all_subd = cmds.ls(type="xgmSubdPatch")
    for subd in all_subd :
        patch = cmds.listConnections("{0}.transform".format(subd))[0]
        config_dir[patch] = subd


    pprint(config_dir)
    return config_dir


def getShapeNode(sdNode):
    mselectionList = om.MSelectionList()
    mselectionList.add(sdNode)
    dagPath = mselectionList.getDagPath(0)
    shapeNodePath = dagPath.extendToShape()
    fullName = shapeNodePath.fullPathName()
    return fullName


def isGuide(sdnode):
    if cmds.listConnections(sdnode, type="xgmModifierGuide") :
        return True
    else :
        return False

def doCreateGeoCache(fileDir, fileName, node) :
    '''
    Description:
     Create cache files on disk for the selected shape(s) according
     to the specified flags described below.

    $version == 1:
     $args[0] = time range mode:
         time range mode = 0 : use $args[1] and $args[2] as start-end
         time range mode = 1 : use render globals
         time range mode = 2 : use timeline
     $args[1] = start frame (if time range mode == 0)
     $args[2] = end frame (if time range mode == 0)

    $version == 2:
     $args[3] = cache file distribution, either "OneFile" or "OneFilePerFrame"
     $args[4] = 0/1, whether to refresh during caching
     $args[5] = directory for cache files, if "", then use project data dir
     $args[6] = 0/1, whether to create a cache per geometry
     $args[7] = name of cache file. An empty string can be used to specify that an auto-generated name is acceptable.
     $args[8] = 0/1, whether the specified cache name is to be used as a prefix
    $version == 3:
     $args[9] = action to perform: "add", "replace", "merge", "mergeDelete" or "export"
     $args[10] = force save even if it overwrites existing files
     $args[11] = simulation rate, the rate at which the cloth simulation is forced to run
     $args[12] = sample mulitplier, the rate at which samples are written, as a multiple of simulation rate.

     $version == 4:
     $args[13] = 0/1, whether modifications should be inherited from the cache about to be replaced. Valid
                 only when $action == "replace".
     $args[14] = 0/1, whether to store doubles as floats
     $version == 5:
     $args[15] = name of cache format
     $version == 6:
     $args[16] = 0/1, whether to export in local or world space
     '''
    cmds.select(node)
    cmdA = 'doCreateGeometryCache 6 '
    cmdB = '{ "2", "1", "10", "OneFile", "1", '
    cmdC = '"{0}","0","{1}"'.format(fileDir, fileName)
    cmdD = ',"0", "export", "1", "1", "1","0","0","mcx","0" }'
    fullCommand = cmdA+cmdB+cmdC+cmdD
    fullPath = os.path.join(fileDir, fileName)
    mel.eval(fullCommand)
    return fullPath

def doImportGeometryCache(fileName, mesh) :
    print fileName
    pmc.mel.doImportCacheFile(fileName, "mcx", [mesh], list())

def sortNodes(totalList) :
    group_list = []
    for i in totalList :
        pName = cmds.getAttr("{0}.parent_node".format(i))
        ppname = cmds.listRelatives(pName, parent=True)[0]
        ppAssetName = cmds.getAttr("{0}.asset_name".format(ppname))
        parentName = "_".join(cmds.getAttr("{0}.parent_node".format(i)).split("|")[-1].split(":"))
        if not cmds.objExists(parentName) :
            groupNode = cmds.group(em=True, name=parentName)
            cmds.addAttr(groupNode,ln="asset_label", dt="string")
            cmds.addAttr(groupNode, ln="type", dt="string")
            cmds.setAttr("{0}.asset_label".format(groupNode), ppAssetName, type="string")
            cmds.setAttr("{0}.type".format(groupNode), "xgen", type="string")

            cmds.parent(i, parentName)
        else :
            cmds.parent(i, parentName)
        group_list.append(groupNode)
    return group_list



def mainExport(fileDir) :
    tmp_list = []
    total_list = []
    mayafileName = pmc.sceneName()
    basefileName =  mayafileName.basename()
    fileVersion = basefileName.split("_")[-1].split(".")[0]



    # group_dir = createTemplate()
    # print group_dir
    config = baseConfig()
    for mesh in config :
        dirName = fileDir
        if platform.system() == "Windows":
            if "\\" in dirName:
                dirName = "/".join(dirName.split('\\'))
        print "{0}-------->{1}".format(mesh, dirName)
        xgen_parentGroup = cmds.listRelatives(mesh, parent=True)[0]
        asset_group = cmds.listRelatives(xgen_parentGroup, parent=True)[0]
        name_x = asset_group.split(":")[-1]+"_{0}".format(fileVersion)
        xgen_ctl = cmds.listConnections(xgen_parentGroup, type="transform")[0]
        if cmds.getAttr("{0}.hair_vis".format(xgen_ctl)) == 0 :
            cmds.setAttr("{0}.hair_vis".format(xgen_ctl), 1)
        if not cmds.getAttr("{0}.visibility".format(mesh)) :
            try :
                cmds.setAttr("{0}.visibility".format(mesh), True)
            except :
                pass
        meshParent = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
        fileName = mesh
        fileName = fileName.split(":")[-1]
        dirName = os.path.join(dirName, name_x)
        if not os.path.exists(dirName) :
            os.makedirs(dirName)
        if platform.system() == "Windows" :
            if "\\" in dirName :
                dirName = "/".join(dirName.split("\\"))
        print fileName+"/"+dirName
        doCreateGeoCache(dirName, fileName, mesh)
        print "Done"



def mainImport(xmlPath, xmlName) :
    om.MGlobal.displayInfo(" ### start import cache ### ")
    xmlFileName = xmlPath
    localSystem = platform.system()
    if localSystem == "Linux" :
        if cmds.objExists(xmlName) :

            meshShape = getShapeNode(xmlName)
            pmc.mel.doImportCacheFile(xmlPath, "mcx", [meshShape], [])
        else :
            om.MGlobal.displayError("{0} is not exsist".format(xmlName))
    else :
        if "\\" in xmlFileName :
            xmlFileName = "/".join(xmlFileName.split("\\"))
        if cmds.objExists(xmlName) :

            meshShape = getShapeNode(xmlName)
            baseName = xmlFileName.split("/")[-1].split(".")[0]
            pmc.mel.doImportCacheFile(xmlFileName, "mcx", [meshShape], [])
        else :
            om.MGlobal.displayError("{0} is not exsist".format(xmlName))





def initializeFolder_export() :
    scenename = str(pmc.sceneName())
    userBranch = os.path.join(os.path.abspath(os.path.join(scenename, "../../../../..")), "user")
    sharedBranch = os.path.join(os.path.abspath(os.path.join(scenename, "../../../..")), "SHARED/CFX/cache")
    print sharedBranch
    if "\\" in sharedBranch :
        sharedBranch = "/".join(sharedBranch.split("\\"))
    if not os.path.exists(sharedBranch) :
        os.makedirs(sharedBranch)
    return sharedBranch

def initializeFolder_import() :
    scenename = str(pmc.sceneName())
    userBranch = os.path.join(os.path.abspath(os.path.join(scenename, "../../../../..")), "user")
    sharedBranch = os.path.join(os.path.abspath(os.path.join(scenename, "../../../../..")), "SHARED/CFX/cache")
    if "\\" in sharedBranch :
        sharedBranch = "/".join(sharedBranch.split("\\"))
    if not os.path.exists(sharedBranch) :
        os.makedirs(sharedBranch)
    return sharedBranch

def callExportDialog() :
    baseFolder = initializeFolder_export()
    exportFile = cmds.fileDialog2(dialogStyle=2, fm=3, dir=baseFolder)
    if exportFile :
        if os.path.exists(exportFile[0]) :
            print exportFile[0]
            mainExport(exportFile[0])
        else :
            om.MGlobal.displayError("{0} is not exsist".format(exportFile[0]))
    else :
        om.MGlobal.displayWarning("directory is null")


def callImportDialog() :
    basicFilter = "*.xml"
    baseFolder = initializeFolder_import()
    importFile = cmds.fileDialog2(fileFilter = basicFilter, dialogStyle=2, fm=3, dir=baseFolder)

    if importFile :
        if os.path.exists(importFile[0]) :
            asset_name = importFile[0].split("/")[-1].split("_")[0]
            fileList = os.listdir(importFile[0])
            header_nodes = [hnode for hnode in cmds.ls(assemblies=True) if cmds.attributeQuery("asset_hair", node=hnode, exists=True)]
            for hNode in header_nodes :
                patches = cmds.listRelatives(hNode, children=True)
                for patch in patches :
                    if cmds.attributeQuery("description_file", node=patch, exists=True) :

                        xmlFileName = "{0}.xml".format(cmds.getAttr("{0}.description_file".format(patch)))
                        fullXmlPath = os.path.join(importFile[0], xmlFileName)
                        if "\\" in fullXmlPath :
                            fullXmlPath = "/".join(fullXmlPath.split("\\"))
                        patchShape = getShapeNode(patch)
                        pmc.mel.doImportCacheFile(fullXmlPath, "mcx", [patchShape], [])









def importAlexFur() :
    fileName = "alexmason_fur_v016"
    if platform.system() == "Linux" :
        alex_fileName = "/dd/shows/CODM/ASSETDEV/alexmason/SHARED/CFX/fur/{0}.ma".format(fileName)
    else :
        alex_fileName = "T:/shows/CODM/ASSETDEV/alexmason/SHARED/CFX/fur/{0}.ma".format(fileName)
    cmds.file(alex_fileName,
              i=True,
              type="mayaAscii",
              iv=True,
              mnc=True,
              ns=fileName,
              options="v=0",
              preserveReferences=True,
              importFrameRate=True,
              itr="keep")

def importDavidFur() :
    fileName = "davidmason_fur_v006"
    if platform.system() == "Linux":
        david_fileName = "/dd/shows/CODM/ASSETDEV/davidmason/SHARED/CFX/fur/{0}.ma".format(fileName)
    else:
        david_fileName = "T:/shows/CODM/ASSETDEV/davidmason/SHARED/CFX/fur/{0}.ma".format(fileName)
    cmds.file(david_fileName,
              i=True,
              type="mayaAscii",
              iv=True,
              mnc=True,
              ns=fileName,
              options="v=0",
              preserveReferences=True,
              importFrameRate=True,
              itr="keep")

def importGhostFur() :
    fileName = "ghost_hair"
    if platform.system() == "Linux":
        ghost_fileName = "/dd/shows/CODM/ASSETDEV/ghost/SHARED/CFX/fur/{0}.ma".format(fileName)
    else:
        ghost_fileName = "T:/shows/CODM/ASSETDEV/ghost/SHARED/CFX/fur/{0}.ma".format(fileName)
    cmds.file(ghost_fileName,
              i=True,
              type="mayaAscii",
              iv=True,
              mnc=True,
              ns=fileName,
              options="v=0",
              preserveReferences=True,
              importFrameRate=True,
              itr="keep")








