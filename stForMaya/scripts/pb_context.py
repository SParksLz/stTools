# -*- coding: utf-8 -*-
# @Author: liuz
# @Date:   2019-09-05 11:14:39
# @Last Modified by:   liuz
# @Last Modified time: 2019-09-05 11:15:33


import maya.cmds as cmds
# import pymel.core as pmc
from contextlib import contextmanager

# cmds.setAttr("{0}.panZoomEnabled".format(cameraShapeName), 0)

@contextmanager
def renderSetting(cameraName) :

    '''
    get old render setting
    '''
    #default render globals setting
    old_cm = cmds.colorManagementPrefs(q=True, outputTransformEnabled=True)
    old_renderer = cmds.getAttr("defaultRenderGlobals.currentRenderer")
    old_format = cmds.getAttr("defaultRenderGlobals.imageFormat")
    old_range = cmds.getAttr("defaultRenderGlobals.animationRange")
    old_anim_bool = cmds.getAttr("defaultRenderGlobals.animation")
    old_renderFormat = cmds.getAttr("defaultRenderGlobals.imageFormat")
    old_renderpadding = cmds.getAttr("defaultRenderGlobals.extensionPadding")
    #camera setting
    old_panZoom = cmds.getAttr("{0}.panZoomEnabled".format(cameraName))
    #hardware setting
    old_hwMode = cmds.getAttr("hardwareRenderingGlobals.renderMode")
    old_hwEx = cmds.getAttr("defaultHardwareRenderGlobals.extension")

    '''
    set to new render setting
    '''

    cmds.colorManagementPrefs(e=True, outputTransformEnabled=True)
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "mayaHardware2", type="string")
    cmds.setAttr("defaultRenderGlobals.animationRange", 0)
    cmds.setAttr("defaultRenderGlobals.animation", 1)
    cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)
    cmds.setAttr("defaultHardwareRenderGlobals.extension", 4)
    for cam in cmds.ls(cameras=True) :
        if cam == cameraName :  
            cmds.setAttr("{0}.renderable".format(cam), 1)
        else :  
            cmds.setAttr("{0}.renderable".format(cam), 0)
    cmds.setAttr("{0}.panZoomEnabled".format(cameraName), False)
    cmds.setAttr("hardwareRenderingGlobals.renderMode", 3)
    cmds.setAttr("defaultRenderGlobals.imageFormat", 40)


    yield
    print "set attr to old"
    cmds.colorManagementPrefs(e=True, outputTransformEnabled=old_cm)
    cmds.setAttr("defaultRenderGlobals.currentRenderer", old_renderer, type="string")
    cmds.setAttr("defaultRenderGlobals.animation", old_anim_bool)
    cmds.setAttr("defaultRenderGlobals.imageFormat", old_format)
    cmds.setAttr("defaultRenderGlobals.animationRange", old_range)
    cmds.setAttr("{0}.panZoomEnabled".format(cameraName), old_panZoom)
    cmds.setAttr("hardwareRenderingGlobals.renderMode", old_hwMode)
    cmds.setAttr("defaultHardwareRenderGlobals.extension", old_hwEx)
    cmds.setAttr("defaultRenderGlobals.extensionPadding", old_renderpadding)
    cmds.setAttr("hardwareRenderingGlobals.renderMode", old_hwMode)
    cmds.setAttr("defaultHardwareRenderGlobals.extension", old_hwEx)


    # print "finish playblasting"

# #
# #
# #
#     print "start playblasting"
#     start = cmds.playbackOptions(q=1, min=1)
#     end = cmds.playbackOptions(q=1, max=1)
#     for i in range(int(start), int(end)+1) :
#         pmc.ogsRender(frame=i)
    # print cmds.colorManagementPrefs(q=True, outputTransformEnabled=True)
    # start = cmds.playbackOptions(q=1, min=1)
    # end = cmds.playbackOptions(q=1, max=1)
    # despath = "/mnt/pb_output/ddd/k.mov"
    # # print cmds.getAttr("{0}.panZoomEnabled".format(cameraShapeName))
    # cmds.playblast(f=despath,compression="png", format="image", percent=100, forceOverwrite=1, quality=100, startTime=start, endTime=end, width=1920, height=1080)



# cmds.render()