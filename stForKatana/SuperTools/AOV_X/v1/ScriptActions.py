import os
from Katana import NodegraphAPI, DrawingModule, Utils


AOV = { 'Beauty':               { 'channle' : 'RGBA', },
        'Position':             { 'channle' : 'RGBA', },
        'Normal':               { 'channle' : 'RGBA', },
        'Depth':                { 'channle' : 'RGBA', },
        'Diffuse_Direct':       { 'channle' : 'RGBA', },
        'Diffuse_Indirect':     { 'channle' : 'RGBA', },
        'Diffuse_Albedo':       { 'channle' : 'RGBA', },
        'Specular_Direct':      { 'channle' : 'RGBA', },
        'Specular_Indirect':    { 'channle' : 'RGBA', },
        'Specular_Albedo':      { 'channle' : 'RGBA', },
        'Coat_Direct':          { 'channle' : 'RGBA', },
        'Coat_Indirect':        { 'channle' : 'RGBA', },
        'Coat_Albedo':          { 'channle' : 'RGBA', },
        'Transmission_Direct':  { 'channle' : 'RGBA', },
        'Transmission_Indirect':{ 'channle' : 'RGBA', },
        'Transmission_Albedo':  { 'channle' : 'RGBA', },
        'SSS_Direct':           { 'channle' : 'RGBA', },
        'SSS_Indirect':         { 'channle' : 'RGBA', },
        'SSS_Albedo':           { 'channle' : 'RGBA', },
        'Vol_Direct':           { 'channle' : 'RGBA', },
        'Vol_Indirect':         { 'channle' : 'RGBA', },
        'Vol_Albedo':           { 'channle' : 'RGBA', },
        'crypto_object':        { 'channle' : 'RGBA', },
        'crypto_material':      { 'channle' : 'RGBA', },
        }

def connectAOVnode(AOCDnode,RODnode):
        A = AOCDnode.getOutputPortByIndex(0)
        B = RODnode.getInputPortByIndex(0)
        A.connect(B)


def ROD_setparameter(node, outputname, ctype, channel):
        node.getParameter('outputName').setValue('%s' %(outputname), 0)
        with NodegraphAPI.InteractiveContext():
                # self._nodeTypeAttr.setValue(str(self._type), NodegraphAPI.GetCurrentTime(), False)
                node.checkDynamicParameters()
                node.getParameter('args.renderSettings.outputs.outputName.type.value').setValue('%s' %(ctype),0)
                node.getParameter('args.renderSettings.outputs.outputName.type.enable').setValue(1, 0)
                node.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.value').setValue('%s' %(channel),0)
                node.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.enable').setValue(1, 0)
                # print 'doooooooooooooooooone!!!!!!!!!!!!!!!'
                # node.getParameter('args.renderSettings.outputs.outputName.locationType.value').setValue('file',0)
                # node.getParameter('args.renderSettings.outputs.outputName.locationType.enable').setValue(1, 0)
                # print 'ssssssssssssssssssssssssss'
                # if len(node.getParameter('args.renderSettings.outputs.outputName.locationSettings').getChildren()) == 1:
                #         node._flushAll()
                #         node.checkDynamicParameters()
                #         node.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.enable').setValue(1,0)
                #         node.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.value').setExpression('%s' %(outputpath),0)
                #         node.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.value').setExpressionFlag(True)


def AOCD_setparameter(node, name, channel, imagetype):
        with NodegraphAPI.InteractiveContext():
                if node.getName().split('_')[0] in ['depth', 'normal', 'position'] :
                    node.getParameter('filter').setValue('closest_filter', 0)
                node.getParameter('name').setValue('%s' %(name), 0)
                node.getParameter('channel').setValue('%s' %(channel), 0)
                node.getParameter('type').setValue('%s' %(imagetype), 0)
                node.flushAll()
                # # node.checkDynamicParameters()
                # node.getParameter('nodes.driverParameters.tiled.enable').setValue(1,0)
                # node.getParameter('nodes.driverParameters.tiled.value').setValue(0.0,0)


def get_passed_nodelist(aovname, parent):
        nodelist = parent.getChildren()
        X_node = []
        for i in nodelist :
                if i.getParent() == parent and i.getName().split('_')[0] == '%s' %(aovname):
                        X_node.append(i)
        return X_node

def set_node_passed(nodelist,v):
        for i in nodelist:
                i.setBypassed(v)
def get_upnode(node):
        port = node.getReturnPort('out')
        upport = port.getConnectedPort(0)
        upnode = upport.getNode()
        return upnode

def set_mergenode_parameter(node, outputpath):
        with NodegraphAPI.InteractiveContext():
                node.checkDynamicParameters()
                node.getParameter('outputName').setValue('AOV_merge',0)
                node.getParameter('args.renderSettings.outputs.outputName.type.enable').setValue(1, 0)
                node.getParameter('args.renderSettings.outputs.outputName.type.value').setValue('merge', 0)
                node.getParameter('args.renderSettings.outputs.outputName.locationType.value').setValue('file',0)
                node.getParameter('args.renderSettings.outputs.outputName.locationType.enable').setValue(1, 0)
                if len(node.getParameter('args.renderSettings.outputs.outputName.locationSettings').getChildren()) == 1:
                        node._flushAll()
                        node.checkDynamicParameters()
                        node.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.enable').setValue(1,0)
                        node.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.value').setExpression('%s' %(outputpath),0)
                        node.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.value').setExpressionFlag(True)
def set_mergeoutput(parent, node):
        children = parent.getChildren()
        all_rod = [x for x in children if x.getType() == 'RenderOutputDefine' and x.isBypassed() == False and x.getParameter('args.renderSettings.outputs.outputName.type.value').getValue(0) != 'merge']
        all_aov = [i.getParameter('outputName').getValue(0) for i in all_rod]
        cccc = ','.join(all_aov)
        with NodegraphAPI.InteractiveContext():
                node.checkDynamicParameters()
                node.getParameter('args.renderSettings.outputs.outputName.mergeOutputs.enable').setValue(1, 0)
                node.getParameter('args.renderSettings.outputs.outputName.mergeOutputs.value').setValue(cccc, 0)

def set_aovs_to_onepath(node, path):
        parameters = node.getParameters()
        children = parameters.getChildren()
        path = '%s' %(path)
        fomat = '%s' %('.####.exr')
        for child in children:
                name_lst = child.getName().split('_')
                if len(name_lst) == 2:
                        name = child.getName().split('_')[0]
                        fullpath = path+name+fomat
                        child.setValue(fullpath,0)

                elif len(name_lst) == 3:
                        name_l = child.getName().split('_')[0:2]
                        name_2 = ''.join(name_l)
                        if name_2 != 'aovmerge':
                                fulln = path+name_2+fomat
                                child.setValue(fulln,0)

def getrod(parent, state):
        children = parent.getChildren()
        all_rod = [child for child in children if child.getType() == 'RenderOutputDefine']
        all_aocd = [x for x in children if x.getType() == 'ArnoldOutputChannelDefine']
        for rod in all_rod:
                if state == 2 :
                        # rod.getParameter('args.renderSettings.outputs.outputName.type.value').setValue('deep',0)
                        with NodegraphAPI.InteractiveContext():
                                rod.getParameter('args.renderSettings.outputs.outputName.locationType.enable').setValue(1, 0)
                                rod.getParameter('args.renderSettings.outputs.outputName.locationType.value').setValue('file',0)
                                rod._flushAll()
                                rod.checkDynamicParameters()
                                rod.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.enable').setValue(1,0)
                                rod.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.value').setExpression('self.getParent().Deep_path' + "+" + "self.getNodeName().split('_')[0]" + "+" + "'"+'_deep/'  + "'" + '+'  + "project.assetID.split('.')[0].split('/')[-1]"+"+"+"'"+'.####.exr' + "'",0)
                                rod.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.value').setExpressionFlag(True)
                if state == 0 :
                        rod.getParameter('args.renderSettings.outputs.outputName.type.value').setValue('color',0)
                        with NodegraphAPI.InteractiveContext():
                                rod.getParameter('args.renderSettings.outputs.outputName.locationType.enable').setValue(1, 0)
                                rod.getParameter('args.renderSettings.outputs.outputName.locationType.value').setValue('local',0)
                                rod._flushAll()
                                rod.checkDynamicParameters()


def set_aocd_parameter(aocdnode, name, channel, lpe):
    with NodegraphAPI.InteractiveContext():
        aocdnode.getParameter('type').setValue('RGB', 0)
        aocdnode.getParameter('name').setExpression('%s' %(name), 0)
        aocdnode.getParameter('name').setExpressionFlag(True)
        aocdnode.getParameter('channel').setExpression('%s' %(channel), 0)
        aocdnode.getParameter('channel').setExpressionFlag(True)
        aocdnode.getParameter('lightPathExpression').setExpression('%s' %(lpe), 0)
        aocdnode.getParameter('lightPathExpression').setExpressionFlag(True)
        aocdnode.flushAll()


def set_rod_parameter(rodnode, name, channel):
    rodnode.getParameter('outputName').setExpression('%s' %(name), 0)
    rodnode.getParameter('outputName').setExpressionFlag(True)
    with NodegraphAPI.InteractiveContext():
        rodnode.checkDynamicParameters()
        rodnode.getParameter('args.renderSettings.outputs.outputName.type.enable').setValue(1,0)
        rodnode.getParameter('args.renderSettings.outputs.outputName.type.value').setValue('color', 0)
        # rodnode.checkDynamicParameters()
        # rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.convertSettings.exrOptimize.enable').setValue(1,0)
        # rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.convertSettings.exrOptimize.value').setValue('No',0)
        rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.value').setExpression('%s' %(channel),0)
        rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.value').setExpressionFlag(True)
        rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.enable').setValue(1, 0)