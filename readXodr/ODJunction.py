
#--surface --> CRG
class JunctionSurfaceCRG(object) :
    def __init__(self, xml_node):
        self.file = xml_node.get("file")
        self.mode = xml_node.get("mode")
        self.purpose = xml_node.get("purpose")
        self.zOffset = xml_node.get("zOffset")
        self.zScale = xml_node.get("zScale")


class JunctionSurface(object):
    def __init__(self, xml_node):
        pass

#--controller
class JunctionController(object):
    def __init__(self, xml_node):
        self.id = xml_node.get("id")
        self.type = xml_node.get("type")
        self.sequence = xml_node.get("sequence")

#--priority
class JunctionPriority(object):
    def __init__(self, xml_node):
        self.high = xml_node.get("high")
        self.low = xml_node.get("low")

#--connection --> predecessor | successor
#             --> lanelink
class JunctionConnectionLaneLink(object):
    def __init__(self, xml_node):
        self.link_from = xml_node.get("from")
        self.link_to = xml_node.get("to")

class JunctionPredecessor(object):
    def __init__(self, xml_node):
        self.elementType = xml_node.get("elementType")
        self.elementId = xml_node.get("elementId")
        self.elementS = xml_node.get("elementS")
        self.elementDir = xml_node.get("elementDir")

class JunctionSuccessor(object):
    def __init__(self, xml_node):
        self.elementType = xml_node.get("elementType")
        self.elementId = xml_node.get("elementId")
        self.elementS = xml_node.get("elementS")
        self.elementDir = xml_node.get("elementDir")

class JunctionConnection(object):
    def __init__(self, xml_node):
        self.id = xml_node.get("id")
        self.type = xml_node.get("type")
        self.incomingRoad = xml_node.get("incomingRoad")
        self.connectionRoad = xml_node.get("connectionRoad")
        self.contactPoint = xml_node.get("contactPoint")