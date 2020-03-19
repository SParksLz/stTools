import maya.cmds as cmds
import pymel.core as pmc
def _createShader() :
    shader = cmds.shadingNode('RedshiftMaterial', asShader=True)

    exAttr = cmds.addAttr(shader, ln="shader_type", dt="string")
    cmds.setAttr("{0}.{1}".format(shader, "shader_type"), 'turntableShaderBall', type='string')

    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    exAttr = cmds.addAttr(shading_group, ln="shader_type", dt="string")
    cmds.setAttr("{0}.{1}".format(shading_group, "shader_type"), 'turntableShaderBall', type='string')
    cmds.connectAttr('{0}.outColor'.format(shader), '{0}.surfaceShader'.format(shading_group))
    shaderBall = cmds.polySphere()



    return shading_group, shaderBall, shader


def _add_turntableShaderBalls() :
    selectionList = cmds.ls(sl=1)
    chromeShader, chromeShaderBall, chromeShaderNode = _createShader()
    chrome_trans = cmds.rename(chromeShaderBall[0], 'chrome')
    lambertShader, lambertShaderBall, lamberShaderNode = _createShader()
    lambert_trans = cmds.rename(lambertShaderBall[0], 'lambert')
    bpShader, bpShaderBall, bpShaderNode = _createShader()
    bp_trans = cmds.rename(bpShaderBall[0], 'blackPlastic')
    wpShader, wpShaderBall, wpShaderNode = _createShader()
    wp_trans = cmds.rename(bpShaderBall[0], 'whitePlastic')
    cmds.select(chrome_trans)
    cmds.sets( e=True, forceElement= chromeShader)
    #cmds.setAttr('{0}.preset'.format(chromeShaderNode), 6)
    cmds.setAttr('{0}.diffuse_weight'.format(chromeShaderNode), 0)
    cmds.setAttr('{0}.refl_roughness'.format(chromeShaderNode), 0)
    cmds.setAttr('{0}.refl_samples'.format(chromeShaderNode), 256)
    cmds.setAttr('{0}.refl_fresnel_mode'.format(chromeShaderNode), 1)
    cmds.setAttr('{0}.refl_reflectivityR'.format(chromeShaderNode), 0.531)
    cmds.setAttr('{0}.diffuse_colorR'.format(lamberShaderNode), 0.5)
    cmds.setAttr('{0}.diffuse_colorG'.format(lamberShaderNode), 0.5)
    cmds.setAttr('{0}.diffuse_colorB'.format(lamberShaderNode), 0.5)
    cmds.setAttr('{0}.refl_weight'.format(lamberShaderNode), 0.0)
    cmds.select(bp_trans)
    cmds.sets( e=True, forceElement= bpShader)
    cmds.setAttr('{0}.diffuse_colorR'.format(bpShaderNode), 0.0)
    cmds.setAttr('{0}.diffuse_colorG'.format(bpShaderNode), 0.0)
    cmds.setAttr('{0}.diffuse_colorB'.format(bpShaderNode), 0.0)
    cmds.select(wp_trans)
    cmds.setAttr('{0}.refl_reflectivityG'.format(chromeShaderNode), 0.512)
    cmds.setAttr('{0}.refl_reflectivityB'.format(chromeShaderNode), 0.493)
    cmds.setAttr('{0}.refl_edge_tintR'.format(chromeShaderNode), 0.571)
    cmds.setAttr('{0}.refl_edge_tintG'.format(chromeShaderNode), 0.540)
    cmds.setAttr('{0}.refl_edge_tintB'.format(chromeShaderNode), 0.592)
    cmds.select(lambert_trans)
    cmds.sets( e=True, forceElement= lambertShader)
    cmds.sets( e=True, forceElement= wpShader)
    cmds.setAttr('{0}.diffuse_colorR'.format(wpShaderNode), 1.0)
    cmds.setAttr('{0}.diffuse_colorG'.format(wpShaderNode), 1.0)
    cmds.setAttr('{0}.diffuse_colorB'.format(wpShaderNode), 1.0)
    newGroup = cmds.createNode('transform')
    newGroup = cmds.rename(newGroup, 'shaderBalls')
    exAttr = cmds.addAttr(newGroup, ln="shader_type", dt="string")
    cmds.setAttr("{0}.{1}".format(newGroup, "shader_type"), 'turntableShaderBall', type='string')
    shaderBalls = [chrome_trans, bp_trans, wp_trans, lambert_trans]
    x_value = 0.0
    for shaderBall in shaderBalls :
        print shaderBall
        x_value += 2.5
        cmds.setAttr("{0}.translateX".format(shaderBall), x_value)
        cmds.parent(shaderBall, newGroup)


def renderSetting(renderableCamera) :

    cmds.setAttr("defaultRenderGlobals.currentRenderer", "redshift", type="string")
    cmds.setAttr("defaultRenderGlobals.animation", 1)
    cmds.setAttr("defaultRenderGlobals.animationRange", 0)
    cmds.setAttr("defaultRenderGlobals.startFrame", 0)
    cmds.setAttr("defaultRenderGlobals.endFrame", 200)
    cmds.setAttr("defaultResolution.width", 1280)
    cmds.setAttr("defaultResolution.height", 720)
    all_cameras = cmds.ls(type='camera')
    for camera in all_cameras :
        if camera==renderableCamera :
            cmds.setAttr("{0}.renderable".format(camera), 1)
        else :
            cmds.setAttr("{0}.renderable".format(camera), 0)


def cleanAll_turntableStuff() :
    all_turnTableNodes = []
    all_nodes = [i.name() for i in pmc.ls() if i.hasAttr('shader_type')]
    for node in all_nodes :
        if cmds.objExists(node) :  
            cmds.delete(node)




def createTurntableDomeLight() :  
    #domeLight = cmds.createNode('RedshiftDomeLight')
    domeLight = cmds.shadingNode( 'RedshiftDomeLight' , asLight=True )
    print domeLight
    domeLightShapeNode = cmds.listRelatives(domeLight, children=True)[0]
    print domeLightShapeNode
    
    
    
    cmds.setAttr('{0}.alphaReplaceEnable'.format(domeLightShapeNode), 1)
    cmds.setKeyframe(domeLight, v=0, at='rotateY', t=101, ott='linear', itt='linear')
    cmds.setKeyframe(domeLight, v=360, at='rotateY', t=150, ott='linear', itt='linear')
    acTaNode = cmds.listConnections(domeLight, type='animCurveTA')[0]
    exAttr = cmds.addAttr(acTaNode, ln="shader_type", dt="string")
    cmds.setAttr("{0}.{1}".format(acTaNode, "shader_type"), 'turntableShaderBall', type='string')
    cmds.addAttr(domeLight, ln="shader_type", dt="string")
    cmds.setAttr("{0}.{1}".format(domeLight, "shader_type"), "turntableShaderBall", type="string")


    return [domeLight, domeLightShapeNode]






