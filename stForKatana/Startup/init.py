from Katana import Utils, Callbacks
from Katana import NodegraphAPI
def Hello(**kwargs):
    from Katana import NodegraphAPI
    import os
    all_render = NodegraphAPI.GetAllNodesByType('Render')
    for render in all_render:
        for parameter in render.getParameter('outputs.types').getChildren():
            if parameter.getValue(0) == 'merge':
                name = parameter.getName()
                path = render.getParameter('outputs.locations.%s'%(name)).getValue(0)
                parent = '/'.join(path.split('/')[:-1])
                if not os.path.exists(parent):
                    os.makedirs(parent)


Callbacks.addCallback(Callbacks.Type.onRenderSetup, Hello)